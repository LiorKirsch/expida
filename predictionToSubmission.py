'''
Created on Sep 17, 2013

@author: lior
'''
import argparse

def writeToLinesToFile(scores, values, searchId, outputFile):
    yx = zip(scores, values)
    yx.sort(reverse=True)
    
    for pair in yx:
#        outputFile.write('%s,%s %f\n' % (searchId, pair[1] ,pair[0] ) )
        outputFile.write('%s,%s\n' % (searchId, pair[1] ) )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create vw files')
    parser.add_argument('-i' ,'--inputfile',  type=str, default=  "vwTemp/output.predictions" )
    args = parser.parse_args()
    
    outputFileName = '%s.submission' % args.inputfile
    
    
    inputFile = open(args.inputfile , 'r')
    outputFile = open(outputFileName ,'w')
    
    last_search_id = None
    last_search_scores = []
    last_search_prop = []
    
    for line in inputFile:
        line = line[:-1] # remove \n at the end of line
        
        seperateBySpace = line.split(' ')
        score = float( seperateBySpace[0] )
        
        seperateByLine = seperateBySpace[1].split('-')
        searchId = seperateByLine[0]
        propId = seperateByLine[1]
        
        if not last_search_id == searchId and last_search_id is not None:
            writeToLinesToFile(last_search_scores, last_search_prop, last_search_id, outputFile)
                
            last_search_scores = []
            last_search_prop = []

        last_search_id = searchId        
        last_search_scores.append(score)
        last_search_prop.append(propId)
    
    # write the lastline
    writeToLinesToFile(last_search_scores, last_search_prop, last_search_id, outputFile)
    
    inputFile.close()
    outputFile.close()