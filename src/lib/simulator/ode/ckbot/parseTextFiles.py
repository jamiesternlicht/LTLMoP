#!/usr/bin/env python

"""
This file contains all the functions needed to parse CKBot simulation related text files.
"""

import ode, xode.parser
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time, copy, sys

from matrixFunctions import *
from loadModules import *

# ROBOT (.ckbot) FILES
def loadRobotData(sim, filename):
	"""
	Loads full robot information from a text file that specifies:
	1. Configuration Matrix.
	2. Relative rotation and translation from the origin, in CKBot length units.
	3. A set of gaits and target gait execution times.
	"""

	# Clear all previous information
	sim.config = "none"
	sim.connM = []
	sim.basepos = []
	sim.baserot = genmatrix(0,1)   # Identity Matrix
	sim.gaits = []

	# Open the text file.
	data = open(filename,"r")

	# Go through the text file line by line.
	reading = "none"
	for line in data:
		linesplit = line.split()

		# If we are currently reading nothing, then we are looking for the next attribute to read.
		if reading == "none" and linesplit != []:
			if linesplit[0] == "ConfigName:":
				reading = "name"
			elif linesplit[0] == "ConnMatrix:":
				reading = "matrix"
			elif linesplit[0] == "RelativeOffset:":
				reading = "offset"
			elif linesplit[0] == "RelativeRotation:":
				reading = "rotation"
			elif linesplit[0] == "ForwardVector:":
				reading = "fwd_vector"
			elif linesplit[0] == "Gaits:":
				reading = "gait"

		# If we are currently reading something, the continue to do so until finished.

		# If we are reading the name of the configuration, then it is simply the word that makes the line under "ConfigName:"
		elif reading == "name":
			sim.config = linesplit[0]
			reading = "none"

		# If we are reading the connectivity matrix, then read the matrix row by row until we reach whitespace.
		elif reading == "matrix":
			if linesplit == []:
				reading = "none"
			else:
				temprow = []
				for num in linesplit:
					temprow.append(int(num))
				sim.connM.append(temprow)

		# If we are reading the relative offset, then simply read the three numbers (x, y, z) in 
		# the line under "RelativeOffset:" and scale by the size of the modules in the simulator.
		elif reading == "offset":
			for num in linesplit:
				sim.basepos.append(sim.cubesize*float(num))
			reading = "none"

		# If we are reading the relative rotation, then we must read through all the rotations specified and
		# create rotation matrices for each rotation and multiply them together in the correct order.
		elif reading == "rotation":
			if linesplit == []:
				reading = "none"
			else:
				angle = int(linesplit[0])*(math.pi/180)
				axis = linesplit[1]
				if axis == "x":
					axis_idx = 1
				elif axis == "y":
					axis_idx = 2
				else:
					axis_idx = 3
				sim.baserot = multmatrix(genmatrix(angle,axis_idx),sim.baserot)

		# Forward vector reading thingy
		elif reading == "fwd_vector":
			if linesplit == []:
				reading = "none"
			else:
				sign = linesplit[0]
				axis = linesplit[1]
				if sign == "+":
					coeff = 1
				else:
					coeff = -1
				
				if axis == "x":
					sim.fwdvec = [coeff*1, 0, 0]
				elif axis == "y":
					sim.fwdvec = [0, coeff*1, 0]
				elif axis == "z":
					sim.fwdvec = [0, 0, coeff*1]

		# If we are reading gaits, it is more complicated. We must ensure to read all the gaits specified.
		# For each gait, we must be able to tell whether the gait is Periodic or Fixed type and 
		# parse it accordingly.

		elif reading == "gait":

			# Read the Proportional control gain specified in the text file.
			if linesplit[0] == "Gain":
				sim.gain = float(linesplit[1])

			# Figure out whether the gaits are fixed or periodic
			if linesplit[0] == "Type":
				sim.gaittype = linesplit[1]
				if sim.gaittype == "Periodic":
					reading = "periodic_gait"
				else:
					reading = "fixed_gait"				  

		# If we are reading periodic gaits, we know our gait table is just 3 lines.
		# The first line is the set of amplitudes (in degrees*100) of each hinge.
		# The second line is the set of frequencies (in rad/s) of each hinge.
		# The third line is the set of phase angles (in degrees*100) of each hinge.
		elif reading == "periodic_gait" and linesplit != []:
			if linesplit[0] == "Gait":
				amplitudes = []
				frequencies = []
				phases = []
				reading = "amplitude"

		elif reading == "amplitude":
			for elem in linesplit:
				amplitudes.append( float(elem)*(math.pi/180.0)*(1/100.0) )
			reading = "frequency"

		elif reading == "frequency":
			for elem in linesplit:
				frequencies.append( float(elem) )
			reading = "phase"

		elif reading == "phase":
			for elem in linesplit:
				phases.append( float(elem)*(math.pi/180.0)*(1/100.0) )
			tempgait = [amplitudes]
			tempgait.append(frequencies)
			tempgait.append(phases)
			sim.gaits.append(tempgait)
			reading = "periodic_gait"

		# If we are reading fixed gaits, the gait table can be an arbitrary number of lines.
		# For each gait we will read all the steps until we find the last line for the gait 
		# (which the time that the gait should loop in).
		elif reading == "fixed_gait" and linesplit != []:
			if linesplit[0] == "Gait":
				gaitrows = []
				gaittime = 0
				reading = "fixed_gait_rows"

		elif reading == "fixed_gait_rows":
			if len(linesplit)==1:
				gaittime = [float(linesplit[0])]
				gaittime.extend(gaitrows)
				sim.gaits.append(gaittime)
				reading = "fixed_gait"
			else:
				temprow = []
				for elem in linesplit:
					temprow.append( float(elem)*(math.pi/180.0)*(1/100.0) )
				gaitrows.append(temprow)

				
# REGION FILES
def loadRegionData(sim, regionfile):
		"""
		Parses a LTLMoP-formatted ".regions" file and creates a data structure to render the region map in the simulator.
		"""

		data = open(regionfile,"r")

		reading_regions = 0
		for line in data:

			# Find when the Regions information is found in the text file (as per LTLMoP format)
			if (line.split().count("Regions:")>0):
				reading_regions = 1
			# Once we have found where the region information begins, parse it in the form:
			# [color info, vertex info] ==> [R, G, B, [x1, y1], [x2, y2], ...] 
			elif (reading_regions == 1 ):
				info = line.split()
				if (len(info)==0):
					reading_regions = 0
				# Do not plot the boundary region.
				elif info[0].lower()=="boundary":
					if info[1]=="poly":
						posx = int(info[2])
						posy = int(info[3])
						vertices = []
						for idx in range(9,len(info),2):
							vertices.append([posx + int(info[idx]), posy + int(info[idx+1])])
						sim.boundary_data = vertices
					elif info[1]=="rect":
						posx = int(info[2])
						posy = int(info[3])
						width = int(info[4])
						height = int(info[5])
						vertices = []
						vertices.append([posx, posy])
						vertices.append([posx, posy + height])
						vertices.append([posx + width, posy + height])
						vertices.append([posx + width, posy])
						sim.boundary_data = vertices
				elif info[0].lower()!="boundary":
					# Polygon-type region -- extract color and all the vertices in the polygon.
					if info[1]=="poly":
						region_color = [float(info[6])/255.0, float(info[7])/255.0, float(info[8])/255.0]
						posx = int(info[2])
						posy = int(info[3])
						vertices = []
						for idx in range(9,len(info),2):
							vertices.append([posx + int(info[idx]), posy + int(info[idx+1])])
						temp_info = region_color
						temp_info.extend(vertices)
						sim.region_data.append(temp_info)

					elif info[1]=="rect":
						region_color = [float(info[6])/255.0, float(info[7])/255.0, float(info[8])/255.0]
						posx = int(info[2])
						posy = int(info[3])
						width = int(info[4])
						height = int(info[5])
						vertices = []
						vertices.append([posx, posy])
						vertices.append([posx, posy + height])
						vertices.append([posx + width, posy + height])
						vertices.append([posx + width, posy])
						temp_info = region_color
						temp_info.extend(vertices)
						sim.region_data.append(temp_info)

def loadRegionHeights(sim, heightmap):

	sim.heightObstacles = []
	sim.heightColors = []
		
	# Go through all the regions in the list and spawn the height obstacles.
	for i in range(len(heightmap)):

		# Unpack data.
		rd = sim.region_data[i]
		x_vals = []
		z_vals = []
		for j in range(3,len(rd)):
			x_vals.append(rd[j][0]*sim.region_calib[0])
			z_vals.append(-rd[j][1]*sim.region_calib[1])
		height = heightmap[i]*sim.cubesize

		# Create the height obstacle for any non-zero height.			
		if height > 0:

			size = [max(x_vals)-min(x_vals),height,max(z_vals)-min(z_vals)]
			pos = [0.5*(max(x_vals)+min(x_vals)), height*0.5, 0.5*(max(z_vals)+min(z_vals))]
			mass = 50000
					
			# Create the obstacle.
			body = ode.Body(sim.world)
			geom = ode.GeomBox(space=sim.space, lengths=size )
			geom.setBody(body)
			geom.setPosition(pos)
			M = ode.Mass()
			M.setBox(mass,size[0],size[1],size[2])
			body.setMass(M)

			# Fix the obstacle to the environment.
			create_fixed_joint(sim, body)

			# Append all these new pointers to the simulator class.
			sim.heightObstacles.append(geom)
			sim.heightColors.append((rd[0],rd[1],rd[2]))
	
	
# OBSTACLE FILES
def loadObstacles(sim,obstaclefile):
	"""
	Loads obstacles from the obstacle text file.
	"""

	# Initiate data structures.
	data = open(obstaclefile,"r")
	obs_sizes = [];
	obs_positions = [];
	obs_masses = [];
	reading = "None"

	# Parse the obstacle text file.
	for line in data:
		linesplit = line.split()
		if linesplit != []:
			if linesplit[0] != "#":
				obs_sizes.append([float(linesplit[0]),float(linesplit[1]),float(linesplit[2])])
				obs_positions.append([float(linesplit[3]),float(linesplit[4]),float(linesplit[5])])
				obs_masses.append(float(linesplit[6]))      

	# Go through all the obstacles in the list and spawn them.
	for i in range(len(obs_sizes)):

		obs_size = obs_sizes[i]
		obs_pos = obs_positions[i]
		obs_mass = obs_masses[i]
				
		# Create the obstacle.
		body = ode.Body(sim.world)
		geom = ode.GeomBox(space=sim.space, lengths=obs_size )
		geom.setBody(body)
		geom.setPosition(obs_pos)
		M = ode.Mass()
		M.setBox(obs_mass,obs_size[0],obs_size[1],obs_size[2])
		body.setMass(M)

		# Append all these new pointers to the simulator class.
		sim._geoms.append(geom)
