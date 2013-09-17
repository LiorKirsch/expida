'''
Created on Aug 14, 2013

@author: lior
'''

import csv
import argparse
import os.path

def writeInVwFormat(label, itemId,features, numericFeatures, featureNames, numericFeaturesNames):
    
    outputString = '%s %s' % (label, itemId)
    featureString = ''
    for featureIndex in range(0, len(features) ):
        if features[featureIndex] is not None:
            featureName = featureNames[featureIndex]
            featureName = featureName.replace(' ','_')
            featureName = featureName.replace('|','*')
            featureName = featureName.replace(':',';')
    
            featureValue = features[featureIndex]
            featureValue = featureValue.replace('|','*')
            featureValue = featureValue.replace(':',';')
            
    #        if not (featureValue == '' or featureValue == ' '):
            featureString = '%s |%s %s' % (featureString, featureName, featureValue)
    outputString = '%s%s' % (outputString, featureString[1:])
    
    featureString = ''
    for featureIndex in range(0, len(numericFeatures) ):
        
        if numericFeatures[featureIndex] is not None:
            featureName = numericFeaturesNames[featureIndex]
            featureName = featureName.replace(' ','_')
            featureName = featureName.replace('|','*')
            featureName = featureName.replace(':',';')
    
            featureValue = numericFeatures[featureIndex]
            featureValue = featureValue.replace('|','*')
            featureValue = featureValue.replace(':',';')
            
    #        if not (featureValue == '' or featureValue == ' '):
            featureString = '%s %s:%s' % (featureString, featureName, featureValue)
        
    outputString = '%s|Numeric %s' % (outputString, featureString[1:])
    
    return outputString

def createFileName(seperationValue, folder, isUnlabeled, fileWriter):
    if isUnlabeled:
        fileName = "unlabeled-%s" % seperationValue
    else:
        fileName = seperationValue
    fileName = os.path.join(folder ,'%s.vw' % fileName)
    if fileName not in fileWriter.keys():
        fileWriter[fileName] = open(fileName, 'w')
        
    return (fileName, fileWriter)
        
    
    
def getLabelFromFields(row_data, score_metric_with_ids,classification=False, ignoreLabel = False):
    keysForScore = score_metric_with_ids.keys()
    
    if ignoreLabel:
        label = ' '
    else:
        if classification:
            label = '-1'
            maxWeight = 0
            for field in keysForScore:
                if row_data[field] == '1':
                    currentWeight = score_metric_with_ids[field]
                    maxWeight = max(maxWeight,  currentWeight)
                    label = '1 %d' % maxWeight
                    
                    
        else:
            maxScore = 0
            for field in keysForScore:
                if row_data[field] == '1':
                    maxScore = max(maxScore,  score_metric_with_ids[field])
                    
            label = '%d' % maxScore
                
    return label
          
def changeFieldNameToIndex(listOfFields, a_dictionary=None, a_list=None):
    
    output = None
    if a_list is not None:
        output = []
        for item in a_list:
            output.append(   listOfFields.index(item)   ) 
            
    if a_dictionary is not None:
        output = {}
        for itemKey in a_dictionary.keys():
            itemIndex = listOfFields.index(itemKey)
            output[itemIndex] = a_dictionary[itemKey]
            
    return output 
            
def concatAndReplaceWithNone(rowData,featureIndecies, valueToReplace):
    featuresConcat = []
    for currentFeatureIndex in featureIndecies:
        currentData = rowData[currentFeatureIndex]
        if currentData == valueToReplace:
            featuresConcat.append( None)
        else:
            featuresConcat.append( currentData )
            
    return featuresConcat
                
def transform2VWStream(dataFileName, outputfile, featureFields,numericFeatureFields, ignore_value, score_metric, itemFields,isTest):
    fileWriter = open(outputfile, 'w')
        
    with open(dataFileName, 'rb') as f:
        reader = csv.reader(f)
        headers = reader.next()
        
        if isTest:
            score_metric_with_ids = {}
        else:
            score_metric_with_ids = changeFieldNameToIndex(headers, a_dictionary=score_metric)
            
        featureIndecies = changeFieldNameToIndex(headers, a_list=featureFields)
        itemIndecies = changeFieldNameToIndex(headers, a_list=itemFields)
        numericFeatureFieldsIndecies = changeFieldNameToIndex(headers, a_list=numericFeatureFields)
        
        for rowData in reader:
            score = getLabelFromFields(rowData, score_metric_with_ids, classification=True, ignoreLabel=isTest)
            
            itemId = ''
            for itemIndex in itemIndecies:
                itemId = '%s-%s' % (itemId, rowData[itemIndex] )
            itemId = itemId[1:]
            
            itemId = '%s-%s' % (itemId,score.replace(' ','_'))
            
            featuresConcat = concatAndReplaceWithNone(rowData,featureIndecies, ignore_value)
            numericFeaturesConcat = concatAndReplaceWithNone(rowData,numericFeatureFieldsIndecies, ignore_value)
            
            
            outputString = writeInVwFormat(score, itemId,featuresConcat,numericFeaturesConcat, featureFields, numericFeatureFields)
                    
            fileWriter.write('%s\n' % outputString)
                
        fileWriter.close()

           

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='create vw files')
    parser.add_argument('-i' ,'--inputfile',  type=str, default=  "small.csv" )
    parser.add_argument('-o' ,'--outputfile',  type=str, default=  "vwTemp/small.vw" )
    parser.add_argument('-t' ,'--test',dest='test',action='store_true', default=False)
    args = parser.parse_args()
    
    #srch_id    date_time    site_id    visitor_location_country_id    visitor_hist_starrating    visitor_hist_adr_usd    prop_country_id    prop_id    prop_starrating    prop_review_score    prop_brand_bool    prop_location_score1    prop_location_score2    prop_log_historical_price    position    price_usd    promotion_flag    srch_destination_id    srch_length_of_stay    srch_booking_window    srch_adults_count    srch_children_count    srch_room_count    srch_saturday_night_bool    srch_query_affinity_score    orig_destination_distance    random_bool    comp1_rate    comp1_inv    comp1_rate_percent_diff    comp2_rate    comp2_inv    comp2_rate_percent_diff    comp3_rate    comp3_inv    comp3_rate_percent_diff    comp4_rate    comp4_inv    comp4_rate_percent_diff    comp5_rate    comp5_inv    comp5_rate_percent_diff    comp6_rate    comp6_inv    comp6_rate_percent_diff    comp7_rate    comp7_inv    comp7_rate_percent_diff    comp8_rate    comp8_inv    comp8_rate_percent_diff    click_bool    gross_bookings_usd    booking_bool
    
    featureFields = ['visitor_location_country_id',   'prop_country_id',   'prop_id',     'prop_brand_bool',    'promotion_flag',   'srch_destination_id',    'srch_adults_count',   'srch_children_count',   'srch_room_count',   'srch_saturday_night_bool',     'random_bool',   'comp1_rate',   'comp1_inv',   'comp2_rate',   'comp2_inv',   'comp3_rate',   'comp3_inv',   'comp4_rate',   'comp4_inv',    'comp5_rate',   'comp5_inv',    'comp6_rate',   'comp6_inv',     'comp7_rate',   'comp7_inv'  ,   'comp8_rate',   'comp8_inv'  ]
    
    numericFeatureFields = ['visitor_hist_starrating',   'visitor_hist_adr_usd', 'prop_starrating',    'prop_review_score',    'prop_location_score1'   , 'prop_location_score2',    'prop_log_historical_price',  'price_usd', 'orig_destination_distance', 'srch_query_affinity_score' ,'srch_booking_window', 'srch_length_of_stay','comp1_rate_percent_diff' ,'comp2_rate_percent_diff', 'comp3_rate_percent_diff','comp4_rate_percent_diff','comp5_rate_percent_diff','comp6_rate_percent_diff','comp7_rate_percent_diff','comp8_rate_percent_diff' ]
    

    #featuresToPersonalize = ['prop_id','srch_destination_id']
    
    ignore_value = 'NULL'
    score_metric = {'click_bool':1   , 'booking_bool':5} # 'gross_bookings_usd'    
    itemFields = ['srch_id' ,'prop_id']

    transform2VWStream(args.inputfile, outputfile = args.outputfile, score_metric = score_metric,featureFields = featureFields,numericFeatureFields=numericFeatureFields,ignore_value= ignore_value,itemFields=itemFields, isTest= args.test)
#    transform2VWStream(dataFileName, dataFolder = 'vwTemp', seperateByField = 'Network' ,labelField = 'Country',featureFields = featureFields, idField = 'InteractionAuthorExternalID', contentThatMarkInteraction = contentThatMarkInteraction)
    
   #####      vw -d expediaVw.vw -p output.predictions
   #####
   #####            
   #####      vw -d expediaVw.vw -c --passes 2 -f expedia.model
   #####      vw -d expediaVw.vw --passes 2 -f expedia.model --loss_function logistic
   #####      vw -i expedia.model -t test.vw -p test.predictions
   