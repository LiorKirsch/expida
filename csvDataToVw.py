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
        
def addFeaturesAndInteractions(featureIndecies, interactionIndecies, rowData, featuresConcat):
    isInteraction = False
    i = 0
    for currentFeatureIndex in featureIndecies:
        currentData = rowData[currentFeatureIndex]
        if currentData in contentThatMarkInteraction:
            currentData = ''
            isInteraction = True
        featuresConcat[i].append( currentData )
        i = i+1
    
    if isInteraction:
        for currentInteractionIndex in interactionIndecies:
            currentData = rowData[currentInteractionIndex]
            featuresConcat[i].append( currentData )
            i = i+1
    
    return featuresConcat
def getLabelAsInt(labelAsString,validLabels, labelOptions ):

    if validLabels is None :
        if labelAsString not in labelOptions:
            labelOptions.append(labelAsString)
        label = labelOptions.index(labelAsString)
    else:
        if labelAsString in validLabels:
            label = validLabels.index(labelAsString)
        else:
            label = validLabels.index('Other')
            
    return (label, labelOptions)
def checkForUniqueOrEmptyLabels(listOfLabels):
    
    uniqueLabels = list(set(listOfLabels))
    
    if len(uniqueLabels) == 2 and '' in uniqueLabels:
        uniqueLabels.remove('')
        
    return uniqueLabels

def checkForLabelUniquenessAndWriteToFile(lastLabels, lastID,featuresConcat, featuresNames, lastSeperationValue, dataFolder, fileWriter,validLabels, labelOptions):
    uniqueLabels = checkForUniqueOrEmptyLabels(lastLabels)
    if len(uniqueLabels) == 1:
        theLabel =  uniqueLabels[0]
        isUnlabeled =   theLabel == ''
        (fileName, fileWriter) = createFileName(lastSeperationValue, dataFolder, isUnlabeled, fileWriter) 
        (theLabel, labelOptions)  = getLabelAsInt(theLabel,validLabels, labelOptions )
        
        outputString = writeInVwFormat(theLabel, lastID,featuresConcat, featuresNames)
    else:
        (fileName, fileWriter) = createFileName('%s-multiLabelUsers' % lastSeperationValue, dataFolder, False, fileWriter) 
        outputString =  '%s,%s' % (lastID, ','.join(uniqueLabels) ) 
    
    fileWriter[fileName].write('%s\n' % outputString)
        
    return (labelOptions, fileWriter)
    
    
def getScoreFromFields(row_data, score_metric_with_ids, minScore = 0):
    keysForScore = score_metric_with_ids.keys()
    
    maxScore = minScore
    for field in keysForScore:
        if row_data[field] == '1':
            maxScore = max(maxScore,  score_metric_with_ids[field])
            
    return maxScore
          
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
                
def transform2VWStream(dataFileName, dataFolder, featureFields,numericFeatureFields, ignore_value, score_metric, itemFields):

    fileWriter = {}
    (fileName, fileWriter) = createFileName('expediaVw', dataFolder, False, fileWriter) 
        
    
    
    with open(dataFileName, 'rb') as f:
        reader = csv.reader(f)
        headers = reader.next()
        
        score_metric_with_ids = changeFieldNameToIndex(headers, a_dictionary=score_metric)
        featureIndecies = changeFieldNameToIndex(headers, a_list=featureFields)
        itemIndecies = changeFieldNameToIndex(headers, a_list=itemFields)
        numericFeatureFieldsIndecies = changeFieldNameToIndex(headers, a_list=numericFeatureFields)
        
        for rowData in reader:
            itemId = ''
            for itemIndex in itemIndecies:
                itemId = '%s-%s' % (itemId, rowData[itemIndex] )
            itemId = itemId[1:]
            
            
            featuresConcat = concatAndReplaceWithNone(rowData,featureIndecies, ignore_value)
            numericFeaturesConcat = concatAndReplaceWithNone(rowData,numericFeatureFieldsIndecies, ignore_value)
            
            score = getScoreFromFields(rowData, score_metric_with_ids)
            outputString = writeInVwFormat(score, itemId,featuresConcat,numericFeaturesConcat, featureFields, numericFeatureFields)
                    
            fileWriter[fileName].write('%s\n' % outputString)
                
        for fileObj in fileWriter.keys():
            fileWriter[fileObj].close()

           

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='create vw files')
    parser.add_argument('-i' ,'--inputfile',  type=str, default=  "small.csv" )
    parser.add_argument('-o' ,'--outputfolder',  type=str, default=  "vwTemp" )
    args = parser.parse_args()
    
    
    #srch_id    date_time    site_id    visitor_location_country_id    visitor_hist_starrating    visitor_hist_adr_usd    prop_country_id    prop_id    prop_starrating    prop_review_score    prop_brand_bool    prop_location_score1    prop_location_score2    prop_log_historical_price    position    price_usd    promotion_flag    srch_destination_id    srch_length_of_stay    srch_booking_window    srch_adults_count    srch_children_count    srch_room_count    srch_saturday_night_bool    srch_query_affinity_score    orig_destination_distance    random_bool    comp1_rate    comp1_inv    comp1_rate_percent_diff    comp2_rate    comp2_inv    comp2_rate_percent_diff    comp3_rate    comp3_inv    comp3_rate_percent_diff    comp4_rate    comp4_inv    comp4_rate_percent_diff    comp5_rate    comp5_inv    comp5_rate_percent_diff    comp6_rate    comp6_inv    comp6_rate_percent_diff    comp7_rate    comp7_inv    comp7_rate_percent_diff    comp8_rate    comp8_inv    comp8_rate_percent_diff    click_bool    gross_bookings_usd    booking_bool
    
    featureFields = ['visitor_location_country_id',   'prop_country_id',   'prop_id',     'prop_brand_bool',    'promotion_flag',   'srch_destination_id',    'srch_adults_count',   'srch_children_count',   'srch_room_count',   'srch_saturday_night_bool',     'random_bool',   'comp1_rate',   'comp1_inv',   'comp2_rate',   'comp2_inv',   'comp3_rate',   'comp3_inv',   'comp4_rate',   'comp4_inv',    'comp5_rate',   'comp5_inv',    'comp6_rate',   'comp6_inv',     'comp7_rate',   'comp7_inv'  ,   'comp8_rate',   'comp8_inv'  ]
    
    numericFeatureFields = ['visitor_hist_starrating',   'visitor_hist_adr_usd', 'prop_starrating',    'prop_review_score',    'prop_location_score1'   , 'prop_location_score2',    'prop_log_historical_price',  'price_usd', 'orig_destination_distance', 'srch_query_affinity_score' ,'srch_booking_window', 'srch_length_of_stay','comp1_rate_percent_diff' ,'comp2_rate_percent_diff', 'comp3_rate_percent_diff','comp4_rate_percent_diff','comp5_rate_percent_diff','comp6_rate_percent_diff','comp7_rate_percent_diff','comp8_rate_percent_diff' ]
    

    ignore_value = 'NULL'
    score_metric = {'click_bool':1   , 'booking_bool':5} # 'gross_bookings_usd'    
    itemFields = ['srch_id' ,'prop_id']

    transform2VWStream(args.inputfile, dataFolder = args.outputfolder, score_metric = score_metric,featureFields = featureFields,numericFeatureFields=numericFeatureFields,ignore_value= ignore_value,itemFields=itemFields)
#    transform2VWStream(dataFileName, dataFolder = 'vwTemp', seperateByField = 'Network' ,labelField = 'Country',featureFields = featureFields, idField = 'InteractionAuthorExternalID', contentThatMarkInteraction = contentThatMarkInteraction)
    
   