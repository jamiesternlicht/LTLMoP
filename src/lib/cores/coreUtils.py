
import math, re, sys, random, os, subprocess, time
from logic import to_cnf



def conjunctsToCNF(conjuncts, isTrans, propList, outFilename, depth):
    
    propListNext = map(lambda s: 'next_'+s, propList)
    
    props = {propList[x]:x+1 for x in range(0,len(propList))}
    propsNext = {propListNext[x]:len(propList)+x+1 for x in range(0,len(propListNext))}
    mapping = {conjuncts[x]:[] for x in range(0,len(conjuncts))}
    
    cnfClauses = []
    transClauses = []
    n = 0
    p = len(props)+len(propsNext)
    
    
        
    for line in conjuncts:
        lineOld = line
        line = re.sub('[\t\n]*','',line)            
        line = re.sub('s\.','',line)
        line = re.sub('e\.','',line)   
        line = re.sub(r'(next\()', r'(next_', line)         
        line = re.sub('\<\>','',line)  
        line = re.sub('\[\]','',line)  
        line = line.strip()
        #training &
        line = line[:-1]
        if line=='':
            continue
        line = re.sub('!', '~', line)
        #line = re.sub('&\s*\n', '', line)
        line = re.sub('[\s]+', ' ', line)        
        line = re.sub('\<-\>', '<=>', line)
        line = re.sub('->', '>>', line)
        line = line.strip() 
        cnf = str(to_cnf(line))
        allClauses = cnf.split("&");
        #associate original conjuncts with CNF clauses
        mapping[lineOld] = mapping[lineOld] + (range(n+1,n+1+len(allClauses)))
        n = n + len(allClauses)
        for clause in allClauses:    
            clause = re.sub('[()]', '', clause)   
            clause = re.sub('[|]', '', clause)           
            clause = re.sub('~', '-', clause)    
            #replace prop names with var numbers
            for k in propsNext.keys():
                clause = re.sub(k,str(propsNext[k]), clause)
            for k in props.keys():
                clause = re.sub(k,str(props[k]), clause)   
            #add trailing 0         
            cnfClauses.append(clause.strip()+" 0\n")
            if isTrans[lineOld]:
                transClauses.append(clause.strip()+" 0\n")
    
        
    
    #Duplicating transition clauses for depth greater than 1        
    for i in range(1,depth):
        transClausesNew = []
        for clause in transClauses:
            newClause = ""
            for c in clause.split():
                intC = int(c)
                if intC is not 0:                    
                    newClause= newClause + str(cmp(intC,0)*(abs(intC)+len(props)*i)) +" "
                else:
                    newClause= newClause +c+" "
            newClause=newClause+"\n"
            transClausesNew.append(newClause)
        j = 0    
        for line in conjuncts:
            if isTrans[line]:                       
                numVarsInTrans = (len(mapping[line]))/i
                mapping[line] = mapping[line] + (map(lambda x: x+len(transClauses), mapping[line][-numVarsInTrans:]))
                j = j + 1
            # add disjuncts to the goal clause (goal is satisfied in at least one of the time steps)
            # assumes goals all contain <> on line (so no line breaks within goals)
            if "<>" in line:
                for v in mapping[line]:
                    newDisjuncts = ""
                    currGoals = cnfClauses[v-1].split()
                    numVarsInGoal = (len(currGoals) - 1)/i
                    
                    for c in currGoals[-(numVarsInGoal+1):-1]:
                        intC = int(c)
                        if intC is not 0:                    
                            newDisjuncts= newDisjuncts + str(cmp(intC,0)*(abs(intC)+len(props)*(i))) +" "
                            
                    # adding disjuncts here
                    cnfClauses[v-1] = newDisjuncts + cnfClauses[v-1]            
                    
                
            
        n = n + len(transClausesNew)
        p = p + len(props)
        cnfClauses = cnfClauses + transClausesNew
        
        
    #write CNFs to file        
    open(outFilename, 'w').close()
    output = open(outFilename, 'a')
    output.write("p cnf "+str(p)+" "+str(n)+"\n")
    output.writelines(cnfClauses)
    output.close()
    return mapping


def cnfToConjuncts(cnfIndices, mapping):
    conjuncts = []
    i = 0
    for k in mapping.keys():
        i = i + 1
        if not set(mapping[k]).isdisjoint(cnfIndices):
            conjuncts.append(k)                
    return conjuncts
