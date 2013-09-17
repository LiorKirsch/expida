'''
Created on Sep 17, 2013

@author: lior
'''
import argparse
import numpy
def calc_dcg(relevance_scores):
    max_iterations = min(38, len(relevance_scores))
    current_dcg_scores = []
    
    for i in xrange(max_iterations):
        this_score = 2^relevance_scores[i] / numpy.log2( i+1 )
        current_dcg_scores.append(     this_score   )
        
    output = sum(current_dcg_scores)
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate evaluation metric')
    parser.add_argument('-i' ,'--inputfile',  type=str, default=  "vwTemp/output.predictions.submission" )
    args = parser.parse_args()
    
    outputFileName = '%s.NDCG' % args.inputfile
    inputFile = open(args.inputfile , 'r')
    outputFile = open(outputFileName , 'w')
    
    last_search_id = None
    last_search_relevance = []
    ndcg_scores = []
    for line in inputFile:
        line = line[:-1] # remove \n at the end of line
        
        seperateBySpace = line.split(',')
        searchId = seperateBySpace[0] 
        propertyId = seperateBySpace[1]
        relevance = seperateBySpace[2]
        
        
        if not last_search_id == searchId and last_search_id is not None:
            
            dcg_score = calc_dcg(last_search_relevance)
                
            sorted_relevance = last_search_relevance.sort(reverse=True)
            idcg_score = calc_dcg(sorted_relevance)
            
            if idcg_score == 0:
                normalized_dcg_score = 0
            else:
                normalized_dcg_score = dcg_score / idcg_score
                
            ndcg_scores.append(normalized_dcg_score)
            outputFile.write('%s,%d\n' % (last_search_id,normalized_dcg_score) )
            
            

        last_search_id = searchId        
        last_search_relevance.append(relevance)
        
        
    print('mean NDCG over %d samples:%f' % (len(ndcg_scores),numpy.mean(ndcg_scores)) )
    inputFile.close()
    outputFile.close()