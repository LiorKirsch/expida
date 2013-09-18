'''
Created on Sep 17, 2013

@author: lior
'''
from __future__ import print_function
import argparse
import numpy
import matplotlib.pyplot as plt

def calc_dcg(relevance_scores):
    max_iterations = min(38, len(relevance_scores))
    current_dcg_scores = []
    
    for i in range(0,max_iterations):
        j = i+1 # starting at 1
        this_score = pow(2,relevance_scores[ i ]) / numpy.log2( j+1 )
        current_dcg_scores.append(     this_score   )
        
    output = sum(current_dcg_scores)
    return output

def calc_ndg(relevance_scores):
    dcg_score = calc_dcg(relevance_scores)
        
    sorted_relevance = sorted(relevance_scores,reverse=True)
    idcg_score = calc_dcg(sorted_relevance)
    
    if idcg_score == 0:
        normalized_dcg_score = 0
    else:
        normalized_dcg_score = dcg_score / idcg_score
        
    return normalized_dcg_score
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculate evaluation metric')
    parser.add_argument('-i' ,'--inputfile',  type=str, default=  "vwTemp/train.predictions.submission" )
    args = parser.parse_args()
    
    outputFileName = '%s.NDCG' % args.inputfile
    inputFile = open(args.inputfile , 'r')
#    outputFile = open(outputFileName , 'w')
    
    last_search_id = None
    last_search_relevance = []
    ndcg_scores = []
    i = 1
    
    inputFile.readline()  # skip the header line
    for line in inputFile:
        line = line[:-1] # remove \n at the end of line
        
        seperateByComma = line.split(',')
        searchId = float(seperateByComma[0]) 
        propertyId = float(seperateByComma[1])
        relevance = float(seperateByComma[2])
        
        
        if not last_search_id == searchId and last_search_id is not None:
            
            normalized_dcg_score = calc_ndg(last_search_relevance)
            ndcg_scores.append(normalized_dcg_score)
#            outputFile.write('%d,%f\n' % (last_search_id,normalized_dcg_score) )
            
            last_search_relevance = []
            

        last_search_id = searchId        
        last_search_relevance.append(relevance)
        i = i + 1
        if numpy.mod(i,100000) == 0:
            print('.', end='')
    
    ############### for the last element ##################
    normalized_dcg_score = calc_ndg(last_search_relevance)
    ndcg_scores.append(normalized_dcg_score)
#    outputFile.write('%d,%f\n' % (last_search_id,normalized_dcg_score) )
    ############### for the last element ##################
    
    
    print('\n mean NDCG over %d searches:%f (+-%f)' % (len(ndcg_scores),numpy.mean(ndcg_scores),numpy.std(ndcg_scores)) )
    print('\n max %f, min %f' % (numpy.max(ndcg_scores),numpy.min(ndcg_scores)) )
    
    hist, bins = numpy.histogram(ndcg_scores,bins = 100)
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.bar(center, hist, align = 'center', width = width)
    plt.show()

    inputFile.close()
    outputFile.close()