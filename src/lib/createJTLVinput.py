""" 
    ===============================================
    createJTLVinput.py - LTL Pre-Processor Routines
    ===============================================
    
    Module that creates the input files for the JTLV based synthesis algorithm.
    Its functions create the skeleton .smv file and the .ltl file which
    includes the topological relations and the given spec.
"""
import math
import parseEnglishToLTL
import textwrap

def createSMVfile(fileName, numRegions, sensorList, robotPropList):
    ''' This function writes the skeleton SMV file.
    It takes as input a filename, the number of regions, the list of the
    sensor propositions and the list of robot propositions (without the regions).
    '''

    fileName = fileName + '.smv'
    smvFile = open(fileName, 'w')

    # Write the header
    smvFile.write(textwrap.dedent("""
    -- Skeleton SMV file
    -- (Generated by the LTLMoP toolkit)


    MODULE main
        VAR
            e : env();
            s : sys();
    """));

    # Define sensor propositions
    smvFile.write(textwrap.dedent("""
    MODULE env -- inputs
        VAR
    """));
    for sensor in sensorList:
        smvFile.write('\t\t')
        smvFile.write(sensor)
        smvFile.write(' : boolean;\n')

    smvFile.write(textwrap.dedent("""
    MODULE sys -- outputs
        VAR
    """));

    # Define the number of bits needed to encode the regions
    numBits = int(math.ceil(math.log(numRegions,2)))
    for bitNum in range(numBits):
        smvFile.write('\t\tbit')
        smvFile.write(str(bitNum))
        smvFile.write(' : boolean;\n')

    # Define robot propositions
    for robotProp in robotPropList:
        smvFile.write('\t\t')
        smvFile.write(robotProp)
        smvFile.write(' : boolean;\n')

    # close the file
    smvFile.close()
    

def createLTLfile(fileName, sensorList, robotPropList, adjData, spec_env, spec_sys):
    ''' This function writes the LTL file. It encodes the specification and 
    topological relation. 
    It takes as input a filename, the list of the
    sensor propositions, the list of robot propositions (without the regions),
    the adjacency data (transition data structure) and
    a specification
    '''

    fileName = fileName + '.ltl'
    ltlFile = open(fileName, 'w')

    numBits = int(math.ceil(math.log(len(adjData),2)))
    bitEncode = parseEnglishToLTL.bitEncoding(len(adjData), numBits)
    currBitEnc = bitEncode['current']
    nextBitEnc = bitEncode['next']
    
    # Write the header and begining of the formula
    ltlFile.write(textwrap.dedent("""
    -- LTL specification file
    -- (Generated by the LTLMoP toolkit)

    """))
    ltlFile.write('LTLSPEC -- Assumptions\n')
    ltlFile.write('\t(\n')

    # TODO: only do this if necessary
    ltlFile.write('\tTRUE & [](TRUE) & []<>(TRUE)\n')

    # Write the environment assumptions
    # from the 'spec' input 
    if spec_env != "":
        ltlFile.write('&' + spec_env)
    ltlFile.write('\n\t);\n\n')

    ltlFile.write('LTLSPEC -- Guarantees\n')
    ltlFile.write('\t(\n')

    # TODO: only do this if necessary
    ltlFile.write('\tTRUE & [](TRUE) & []<>(TRUE) & \n')

    # The topological relation (adjacency)
    for Origin in range(len(adjData)):
        # from region i we can stay in region i
        ltlFile.write('\t\t\t []( (')
        ltlFile.write(currBitEnc[Origin])
        ltlFile.write(') -> ( (')
        ltlFile.write(nextBitEnc[Origin])
        ltlFile.write(')')
        
        for dest in range(len(adjData)):
            if adjData[Origin][dest]:
                # not empty, hence there is a transition
                ltlFile.write('\n\t\t\t\t\t\t\t\t\t| (')
                ltlFile.write(nextBitEnc[dest])
                ltlFile.write(') ')

        # closing this region
        ltlFile.write(' ) ) & \n ')
    
    # Setting the system initial formula to allow only valid
    #  region encoding. This may be redundent if an initial region is
    #  specified, but it is here to ensure the system cannot start from
    #  an invalid encoding
    initreg_formula = '\t\t\t( ' + currBitEnc[0] + ' \n'
    for regionInd in range(1,len(currBitEnc)):
        initreg_formula = initreg_formula + '\t\t\t\t | ' + currBitEnc[regionInd] + '\n'
    initreg_formula = initreg_formula + '\t\t\t) \n'

    ltlFile.write(initreg_formula)

    # Write the desired robot behavior
    if spec_sys != "":
        ltlFile.write('&' + spec_sys)

    # Close the LTL formula
    ltlFile.write('\n\t);\n')

    # close the file
    ltlFile.close()


