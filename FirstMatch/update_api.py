from django.views.decorators.csrf import csrf_exempt
from .models import ModelTests, Adelphoi_Mapping
from rest_framework.parsers import JSONParser
from .serializers import UpdateSerializers
from django.http import JsonResponse
import pandas as pd
import pickle
import os
from AdelphoiProject.settings import SOURCE_DIR
@csrf_exempt
def update_logic(request,pk):
    query = ModelTests.objects.get(pk=pk)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UpdateSerializers(query, data=data)
        if serializer.is_valid(raise_exception=True):
            query_gender = Adelphoi_Mapping.objects.filter(
                gender=serializer.validated_data.get('gender'))
            suggested_programs = []
            unique_list_programs = []
            if query_gender.count() > 0:
                for i in query_gender:
                    suggested_programs.append(i.program_model_suggested)
                    # program_type
                for i in suggested_programs:
                    if i not in unique_list_programs:
                        unique_list_programs.append(i)
            if not serializer.validated_data.get('Exclusionary_Criteria'):
                # logger.info(
                #     'AdelphoiList class where Exclusionary_Criteria is False')
                dt = {'Gender': serializer.validated_data.get('gender'),
                      'AgeAtEnrollStart': serializer.validated_data.get(
                          'ageAtEnrollStart'),
                      'CYF_code': serializer.validated_data.get('CYF_code'),
                      'LS_Type': serializer.validated_data.get('ls_type'),
                      'EpisodeNumber': serializer.validated_data.get(
                          'episode_number'),
                      'RefSourceName': serializer.validated_data.get(
                          'RefSourceCode'),
                      'Number of foster care placements':
                          serializer.validated_data.get(
                          'number_of_foster_care_placements'),
                      'AgeAtEpisodeStart':
                          serializer.validated_data.get('ageAtEpisodeStart'),
                      'Number of prior placements \n(excluding shelter and detention)':
                          serializer.validated_data.get(
                          'number_of_prior_placements'),
                      'Number of prior treatment terminations (excluding shelter or detention)':
                          serializer.validated_data.get(
                              'number_of_prior_treatment_terminations'),
                      'Length of time since living at home':
                          serializer.validated_data.get(
                          'length_of_time_since_living_at_home'),
                      'Termination directly to AV':
                          serializer.validated_data.get(
                              'termination_directly_to_AV'),
                      'Death Caregiver': serializer.validated_data.get(
                          'death_Caregiver'),
                      'Borderline IQ (below 70)':
                          serializer.validated_data.get('borderline_IQ'),
                      'Hist of prior program SAO':
                          serializer.validated_data.get(
                              'hist_of_prior_program_SAO'),
                      'Death Silblings':
                          serializer.validated_data.get('death_Silblings'),
                      'Alcohol Use':
                          serializer.validated_data.get('alcohol_Use'),
                      'Drug Use': serializer.validated_data.get('drug_Use'),
                      'Incarcerated caregivers':
                          serializer.validated_data.get(
                              'incarcerated_caregivers'),
                      'Incarcerated siblings':
                          serializer.validated_data.get(
                              'incarcerated_siblings'),
                      'Number of prior AWOLS':
                          serializer.validated_data.get(
                              'number_of_prior_AWOLS'),
                      'Animal cruelty':
                          serializer.validated_data.get('animal_cruelty'),
                      'Number of prior hospitalizations':
                          serializer.validated_data.get(
                              'prior_hospitalizations'),
                      'Compliant with medication':
                          serializer.validated_data.get('compliant_with_meds'),
                      'Significant mental health symptoms':
                          serializer.validated_data.get(
                          'significant_mental_health_symptoms'),
                      'Severe mental health symptoms':
                          serializer.validated_data.get(
                              'severe_mental_health_symptoms'),
                      'Autism Diagnosis': serializer.validated_data.get(
                          'autism_Diagnosis'),
                      'Borderline Personality':
                          serializer.validated_data.get(
                              'borderline_Personality'),
                      'Psychosis': serializer.validated_data.get('psychosis'),
                      'Reactive Attachment Disorder':
                          serializer.validated_data.get(
                              'reactive_Attachment_Disorder'),
                      'Schizophrenia':
                          serializer.validated_data.get('schizophrenia'),
                      'YLS_PriorCurrentOffenses_Score':
                          serializer.validated_data.get(
                              'yls_PriorCurrentOffenses_Score'),
                      'YLS_FamCircumstances_Score':
                          serializer.validated_data.get(
                              'yls_FamCircumstances_Score'),
                      'YLS_Edu_Employ_Score':
                          serializer.validated_data.get(
                              'yls_Edu_Employ_Score'),
                      'YLS_Peer_Score':
                          serializer.validated_data.get(
                              'yls_Peer_Score'),
                      'YLS_Subab_Score':
                          serializer.validated_data.get('yls_Subab_Score'),
                      'YLS_Leisure_Score':
                          serializer.validated_data.get('yls_Leisure_Score'),
                      'YLS_Personality_Score': serializer.validated_data.get(
                          'yls_Personality_Score'),
                      'YLS_Attitude_Score':
                          serializer.validated_data.get('yls_Attitude_Score'),
                      'Client self-harm':
                          serializer.validated_data.get('client_self_harm'),
                      'CANS_LifeFunctioning':
                          serializer.validated_data.get(
                              'cans_LifeFunctioning'),
                      'CANS_YouthStrengths':
                          serializer.validated_data.get(
                              'cans_YouthStrengths'),
                      'CANS_CareGiverStrengths':
                          serializer.validated_data.get(
                              'cans_CareGiverStrengths'),
                      'CANS_Culture': serializer.validated_data.get(
                          'cans_Culture'),
                      'CANS_YouthBehavior': serializer.validated_data.get(
                          'cans_YouthBehavior'),
                      'CANS_YouthRisk': serializer.validated_data.get(
                          'cans_YouthRisk'),
                      'CANS_Trauma_Exp': serializer.validated_data.get(
                          'cans_Trauma_Exp'),
                      'Family support':
                          serializer.validated_data.get('family_support'),
                      'Level of aggression': serializer.validated_data.get(
                          'level_of_aggression'),
                      'Fire setting': serializer.validated_data.get('fire_setting'),
                      'Abuse, or neglect':
                          serializer.validated_data.get('abuse_neglect'),
                      'Screening tool for Trauma--Total score':
                          serializer.validated_data.get(
                              'Screening_tool_Trauma'),
                      'FAST_FamilyTogetherScore':
                          serializer.validated_data.get(
                              'FAST_FamilyTogetherScore'),
                      'FAST_CaregiverAdvocacyScore':
                          serializer.validated_data.get(
                              'FAST_CaregiverAdvocacyScore')
                      }  #
                # logger.info("values are %s", dt)
                data = pd.DataFrame(dt, index=[0])

                # Impute empty values with mean values

                if data['Family support'][0] is None:
                    if data['Gender'][0] == 1:
                        data['Family support'] = 1.152941  # 1.148148
                    else:
                        data['Family support'] = 0.969027  # 0.963964
                if data['Level of aggression'][0] is None:
                    if data['Gender'][0] == 1:  #
                        data['Level of aggression'] = 2.3636  # 2.369863
                    else:
                        data['Level of aggression'] = 2.052402  # 2.053333
                if data['Fire setting'][0] is None:
                    if data['Gender'][0] == 1:
                        data['Fire setting'] = 0.0649  # 0.068493
                    else:
                        data['Fire setting'] = 0.2096  # 0.213333
                if data['Client self-harm'][0] is None:
                    if data['Gender'][0] == 1:
                        data['Client self-harm'] = 0.4675  # 0.479452
                    else:
                        data['Client self-harm'] = 0.2026  # 0.197309
                if data['CANS_LifeFunctioning'][0] is None:
                    if data['Gender'][0] == 1:
                        data['CANS_LifeFunctioning'] = 13.1038  # 12.945205
                    else:
                        data['CANS_LifeFunctioning'] = 11.4759  # 11.475556

                if data['CANS_YouthStrengths'][0] is None:
                    if data['Gender'][0] == 1:
                        data['CANS_YouthStrengths'] = 13.6800  # 13.704225
                    else:
                        data['CANS_YouthStrengths'] = 13.1454  # 13.157407
                if data['CANS_CareGiverStrengths'][0] is None:
                    if data['Gender'][0] == 1:
                        data['CANS_CareGiverStrengths'] = 10.0757
                        # 10.129032
                    else:
                        data['CANS_CareGiverStrengths'] = 7.0603  # 7.107692
                if data['CANS_Culture'][0] is None:
                    if data['Gender'][0] == 1:
                        data['CANS_Culture'] = 0.0547  # 0.05797
                    else:
                        data['CANS_Culture'] = 0.1457  # 0.148718
                if data['CANS_YouthBehavior'][0] is None:
                    if data['Gender'][0] == 1:
                        data['CANS_YouthBehavior'] = 9.4285  # 9.438356
                    else:
                        data['CANS_YouthBehavior'] = 7.6986  # 7.733333
                if data['CANS_YouthRisk'][0] is None:
                    if data['Gender'][0] == 1:
                        data['CANS_YouthRisk'] = 4.1038  # 4.191781
                    else:
                        data['CANS_YouthRisk'] = 3.9912  # 3.986667
                if data['CANS_Trauma_Exp'][0] is None:
                    if data['Gender'][0] == 1:
                        data['CANS_Trauma_Exp'] = 5.0410  # 5.042857
                    else:
                        data['CANS_Trauma_Exp'] = 4.3349  # 4.360976
                if data['FAST_FamilyTogetherScore'][0] is None:
                    if data['Gender'][0] == 1:
                        data['FAST_FamilyTogetherScore'] = 7.5614  # 7.377358
                    else:
                        data['FAST_FamilyTogetherScore'] = 7.3027  # 7.245283
                if data['FAST_CaregiverAdvocacyScore'][0] is None:
                    if data['Gender'][0] == 1:
                        data['FAST_CaregiverAdvocacyScore'] = 6.5319
                        # 6.674419
                    else:
                        data['FAST_CaregiverAdvocacyScore'] = 6.0120
                        # 5.887500
                if data['YLS_PriorCurrentOffenses_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_PriorCurrentOffenses_Score'] = 0.6750
                        # 0.684211
                    else:
                        data['YLS_PriorCurrentOffenses_Score'] = 0.5913
                        # 0.566667
                if data['YLS_FamCircumstances_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_FamCircumstances_Score'] = 3.7631
                        # 3.750000
                    else:
                        data['YLS_FamCircumstances_Score'] = 2.7956
                        # 2.811111
                if data['YLS_Edu_Employ_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_Edu_Employ_Score'] = 3.0789
                        # 2.944444
                    else:
                        data['YLS_Edu_Employ_Score'] = 2.3655
                        # 2.322222
                if data['YLS_Peer_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_Peer_Score'] = 2.8947
                        # 2.833333
                    else:
                        data['YLS_Peer_Score'] = 1.9462
                        # 1.944444
                if data['YLS_Subab_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_Subab_Score'] = 2.1578
                        # 2.166667
                    else:
                        data['YLS_Subab_Score'] = 1.301
                        # 1.311111
                if data['YLS_Leisure_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_Leisure_Score'] = 1.943
                        # 1.944444
                    else:
                        data['YLS_Leisure_Score'] = 2.00
                        # 2.000000
                if data['YLS_Personality_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_Personality_Score'] = 3.5789
                        # 3.555556
                    else:
                        data['YLS_Personality_Score'] = 3.1935
                        # 3.188889
                if data['YLS_Attitude_Score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['YLS_Attitude_Score'] = 1.8947
                        # 1.944444
                    else:
                        data['YLS_Attitude_Score'] = 1.3978
                        # 1.377778
                if data['Screening tool for Trauma--Total score'][0] is None:
                    if data['Gender'][0] == 1:
                        data['Screening tool for Trauma--Total score'] = \
                            14.7555  # 14.595238
                    else:
                        data['Screening tool for Trauma--Total score'] = \
                            14.7244  # 14.634409
                data['LS_Type'].fillna(data['LS_Type'].mode()[0], inplace=True)
                data['LS_Type'] = data['LS_Type'].astype('int')
                dummies = pd.DataFrame()
                for column in ['Gender', 'LS_Type', 'CYF_code']:
                    # ,'RefSourceName'
                    dummies1 = pd.get_dummies(data[column], prefix=column)
                    dummies[dummies1.columns] = dummies1.copy(deep=False)

                cols = ['Gender_1', 'Gender_2', 'LS_Type_1', 'LS_Type_2',
                        'LS_Type_3','LS_Type_4','LS_Type_5','CYF_code_0','CYF_code_1',
                        'CYF_code_2']
                for col in cols:
                    if col in dummies.columns:
                        print('present', col)
                    else:
                        dummies[col] = 0
                data.fillna(0, inplace=True)
                numeric_cols = ['Gender', 'LS_Type', 'CYF_code',
                                'RefSourceName','EpisodeNumber',
                                'Number of foster care placements',
                                'AgeAtEpisodeStart',
                                'Number of prior placements \n(excluding shelter and detention)',
                                'AgeAtEnrollStart',
                                'Number of prior treatment terminations (excluding shelter or detention)',
                                'Length of time since living at home',
                                'Termination directly to AV',
                                'Death Caregiver', 'Borderline IQ (below 70)',
                                'Hist of prior program SAO',
                                'Death Silblings', 'Alcohol Use', 'Drug Use',
                                'Incarcerated caregivers',
                                'Incarcerated siblings',
                                'Number of prior AWOLS',
                                'Animal cruelty',
                                'Number of prior hospitalizations',
                                'Compliant with medication',
                                'Significant mental health symptoms',
                                'Severe mental health symptoms',
                                'Autism Diagnosis', 'Borderline Personality',
                                'Psychosis',
                                'Reactive Attachment Disorder',
                                'Schizophrenia']

                # converting float to integer
                for col in numeric_cols:
                    data[col] = pd.to_numeric(
                        data[col], errors='coerce', downcast='integer')
                ###
                Feature_names = ['EpisodeNumber', 'Number of foster care placements',
                                 'AgeAtEpisodeStart',
                                 'Number of prior placements \n(excluding shelter and detention)',
                                 'Number of prior treatment terminations (excluding shelter or detention)',
                                 'Length of time since living at home',
                                 'Termination directly to AV',
                                 'Death Caregiver', 'Borderline IQ (below 70)',
                                 'Hist of prior program SAO',
                                 'Death Silblings', 'Alcohol Use', 'Drug Use',
                                 'Incarcerated caregivers',
                                 'Incarcerated siblings', 'Number of prior AWOLS',
                                 'Animal cruelty',
                                 'Number of prior hospitalizations',
                                 'Compliant with medication',
                                 'Significant mental health symptoms',
                                 'Severe mental health symptoms',
                                 'Autism Diagnosis', 'Borderline Personality',
                                 'Psychosis',
                                 'Reactive Attachment Disorder',
                                 'Schizophrenia',
                                 'YLS_PriorCurrentOffenses_Score',
                                 'YLS_FamCircumstances_Score',
                                 'YLS_Edu_Employ_Score', 'YLS_Peer_Score',
                                 'YLS_Subab_Score',
                                 'YLS_Leisure_Score', 'YLS_Personality_Score',
                                 'YLS_Attitude_Score',
                                 'Client self-harm',
                                 'CANS_LifeFunctioning',
                                 'CANS_YouthStrengths', 'CANS_CareGiverStrengths',
                                 'CANS_Culture',
                                 'CANS_YouthBehavior', 'CANS_YouthRisk',
                                 'CANS_Trauma_Exp', 'Family support',
                                 'Level of aggression', 'Fire setting',
                                 'Abuse, or neglect',
                                 'Screening tool for Trauma--Total score']

                Xtest = pd.DataFrame(data[Feature_names])
                Xtest[dummies.columns] = dummies

                level_model = pickle.load(
                    open(os.path.join(SOURCE_DIR, "new_pickles","R_LR_LC_11march.sav"),"rb"))
                program_model = pickle.load(
                    open(os.path.join(SOURCE_DIR, "new_pickles","R_DT_P_11march.sav"),
                         "rb"))
                facility_model = pickle.load(
                    open(os.path.join(SOURCE_DIR, "new_pickles","R_LR_FT_11march.sav"),
                         "rb"))
                PC_model = pickle.load(
                    open(os.path.join(SOURCE_DIR, "new_pickles","R_LR_PC_11march.sav"),
                         "rb"))

                level_pred = level_model.predict(Xtest)
                program_pred = program_model.predict(Xtest)
                facility_preds = facility_model.predict(Xtest)
                query = Adelphoi_Mapping.objects.filter(
                    program=program_pred,
                    gender=serializer.validated_data.get('gender'),
                    level_of_care=level_pred, facility_type=facility_preds
                )

                def program_condition(
                        condition_program,level_pred,facility_preds):
                    # logger.info('program_condition function')
                    Xp = pd.DataFrame(
                        data[['EpisodeNumber', 'Number of foster care placements',
                              'AgeAtEpisodeStart',
                              'Number of prior placements \n(excluding shelter and detention)',
                              'Number of prior treatment terminations (excluding shelter or detention)',
                              'Length of time since living at home',
                              'Termination directly to AV',
                              'Death Caregiver', 'Borderline IQ (below 70)',
                              'Hist of prior program SAO',
                              'Death Silblings', 'Alcohol Use', 'Drug Use',
                              'Incarcerated caregivers',
                              'Incarcerated siblings', 'Number of prior AWOLS',
                              'Animal cruelty',
                              'Number of prior hospitalizations',
                              'Compliant with medication',
                              'Significant mental health symptoms',
                              'Severe mental health symptoms',
                              'Autism Diagnosis', 'Borderline Personality',
                              'Psychosis',
                              'Reactive Attachment Disorder',
                              'Schizophrenia']])

                    Xp['Program'] = condition_program
                    Xp['Level_of_Care'] = level_pred
                    Xp['FacilityType'] = facility_preds
                    Xp[dummies.columns] = dummies
                    PC_proba = PC_model.predict_proba(Xp)
                    if PC_proba[0][1] > (0.5):
                        Xp['ProgramCompletion'] = 1
                    else:
                        Xp['ProgramCompletion'] = 0
                    roc_model = pickle.load(open(
                        os.path.join(SOURCE_DIR, "new_pickles","R_LR_RC_11march.sav"),"rb"))
                    roc_result = roc_model.predict_proba(Xp)
                    print("roc_result", roc_result)
                    return [round(PC_proba[0][1] * 100), round(roc_result[0][1] * 100)]

                program_list = []
                level_list = []
                facility_names = []
                program_num = []
                program_model_suggested_list = []
                unique_program_model_suggested_list = []

                if query.count() > 0:
                    if serializer.validated_data.get('gender') == 1:
                        # logger.info('where Exclusionary_Criteria-False, gender-1,condition_program-3')
                        condition_program = 3
                        query2 = Adelphoi_Mapping.objects.filter(program=condition_program,
                                                                 gender=serializer.validated_data.get('gender'),
                                                                 level_of_care=level_pred, facility_type=facility_preds)

                        for i in query2:
                            program_num.append(i.program)
                            program_list.append(i.program_name)
                            level_list.append(i.level_names)
                            facility_names.append(i.facility_names)
                            program_model_suggested_list.append(i.program_model_suggested)
                            # program_type.append(i.program_type)
                        for i in program_model_suggested_list:
                            if i not in unique_program_model_suggested_list:
                                unique_program_model_suggested_list.append(i)

                        query_default = Adelphoi_Mapping.objects.filter(
                            program_model_suggested=program_model_suggested_list[0],
                            default_level_facility=True)
                        level_default = []
                        facility_default = []
                        for i in query_default:
                            level_default.append(i.level_of_care)
                            facility_default.append(i.facility_type)
                        confidence = program_condition(condition_program, level_default[0], facility_default[0])[0]
                        roc_confidence = program_condition(condition_program, level_default[0], facility_default[0])[1]
                        serializer.save(roc_confidence=roc_confidence, program=program_num[0],
                                        condition_program=condition_program,
                                        confidence=confidence, family_support=data['Family support'][0],
                                        level_of_aggression=data['Level of aggression'][0],
                                        fire_setting=data['Fire setting'][0],
                                        client_self_harm=data['Client self-harm'][0],
                                        cans_LifeFunctioning=data['CANS_LifeFunctioning'][0],
                                        cans_YouthStrengths=data['CANS_YouthStrengths'][0],
                                        cans_CareGiverStrengths=data['CANS_CareGiverStrengths'][0],
                                        cans_Culture=data['CANS_Culture'][0],
                                        cans_YouthBehavior=data['CANS_YouthBehavior'][0],
                                        cans_YouthRisk=data['CANS_YouthRisk'][0],
                                        cans_Trauma_Exp=data['CANS_Trauma_Exp'][0],
                                        yls_PriorCurrentOffenses_Score=data['YLS_PriorCurrentOffenses_Score'][0],
                                        yls_FamCircumstances_Score=data['YLS_FamCircumstances_Score'][0],
                                        yls_Edu_Employ_Score=data['YLS_Edu_Employ_Score'][0],
                                        yls_Peer_Score=data['YLS_Peer_Score'][0],
                                        yls_Subab_Score=data['YLS_Subab_Score'][0],
                                        yls_Leisure_Score=data['YLS_Leisure_Score'][0],
                                        yls_Personality_Score=data['YLS_Personality_Score'][0],
                                        yls_Attitude_Score=data['YLS_Attitude_Score'][0],
                                        Screening_tool_Trauma=data['Screening tool for Trauma--Total score'][0],
                                        FAST_FamilyTogetherScore=data['FAST_FamilyTogetherScore'][0],
                                        FAST_CaregiverAdvocacyScore=data['FAST_CaregiverAdvocacyScore'][0],
                                        inclusionary_criteria=serializer.validated_data.get(
                                            'inclusionary_criteria'),
                                        model_program=program_model_suggested_list[
                                            0])  # confidence = PC_proba[0][1]*100

                        return JsonResponse(
                            {"model program": int(program_pred[0]), "program": int(program_pred[0]),
                             "Level of care": int(level_pred[0]),
                             "program_type": unique_program_model_suggested_list, #program_model_suggested_list
                             "Facility Type": int(facility_preds[0]),
                             "gender": int(serializer.validated_data.get('gender')),
                             "Confidence": confidence, "Roc_confidence": roc_confidence,
                             "list_program_types": unique_list_programs})
                    else:
                        if serializer.validated_data.get('inclusionary_criteria') == True:
                            # logger.info(
                            #     'where Exclusionary_Criteria-False, gender-1,inclusionary_criteria=true,condition_program-2')
                            condition_program = 2
                            query3 = Adelphoi_Mapping.objects.filter(program=condition_program,
                                                                     gender=serializer.validated_data.get('gender'),
                                                                     level_of_care=level_pred,
                                                                     facility_type=facility_preds)
                            for i in query3:
                                program_num.append(i.program)
                                program_list.append(i.program_name)
                                level_list.append(i.level_names)
                                facility_names.append(i.facility_names)
                                # program_type.append(i.program_type)
                                program_model_suggested_list.append(i.program_model_suggested)
                            for i in program_model_suggested_list:
                                if i not in unique_program_model_suggested_list:
                                    unique_program_model_suggested_list.append(i)
                            query_default = Adelphoi_Mapping.objects.filter(
                                program_model_suggested=program_model_suggested_list[0],
                                default_level_facility=True)
                            level_default = []
                            facility_default = []
                            for i in query_default:
                                level_default.append(i.level_of_care)
                                facility_default.append(i.facility_type)
                            confidence = program_condition(condition_program, level_default[0], facility_default[0])[0]
                            roc_confidence = \
                            program_condition(condition_program, level_default[0], facility_default[0])[1]
                            serializer.save(roc_confidence=roc_confidence, program=program_num[0],
                                            condition_program=condition_program,
                                            confidence=confidence,
                                            family_support=data['Family support'][0],
                                            level_of_aggression=data['Level of aggression'][0],
                                            fire_setting=data['Fire setting'][0],
                                            client_self_harm=data['Client self-harm'][0],
                                            cans_LifeFunctioning=data['CANS_LifeFunctioning'][0],
                                            cans_YouthStrengths=data['CANS_YouthStrengths'][0],
                                            cans_CareGiverStrengths=data['CANS_CareGiverStrengths'][0],
                                            cans_Culture=data['CANS_Culture'][0],
                                            cans_YouthBehavior=data['CANS_YouthBehavior'][0],
                                            cans_YouthRisk=data['CANS_YouthRisk'][0],
                                            cans_Trauma_Exp=data['CANS_Trauma_Exp'][0],
                                            yls_PriorCurrentOffenses_Score=data['YLS_PriorCurrentOffenses_Score'][0],
                                            yls_FamCircumstances_Score=data['YLS_FamCircumstances_Score'][0],
                                            yls_Edu_Employ_Score=data['YLS_Edu_Employ_Score'][0],
                                            yls_Peer_Score=data['YLS_Peer_Score'][0],
                                            yls_Subab_Score=data['YLS_Subab_Score'][0],
                                            yls_Leisure_Score=data['YLS_Leisure_Score'][0],
                                            yls_Personality_Score=data['YLS_Personality_Score'][0],
                                            yls_Attitude_Score=data['YLS_Attitude_Score'][0],
                                            Screening_tool_Trauma=data['Screening tool for Trauma--Total score'][0],
                                            FAST_FamilyTogetherScore=data['FAST_FamilyTogetherScore'][0],
                                            FAST_CaregiverAdvocacyScore=data['FAST_CaregiverAdvocacyScore'][0],
                                            inclusionary_criteria=serializer.validated_data.get(
                                                'inclusionary_criteria'), model_program=program_model_suggested_list[0])
                            return JsonResponse(
                                {"model program": int(program_pred[0]), "program": int(condition_program),
                                 "Level of care": int(level_pred[0]),
                                 "program_type": unique_program_model_suggested_list,#program_model_suggested_list,
                                 "Facility Type": int(facility_preds[0]),
                                 "gender": int(serializer.validated_data.get('gender')),
                                 "Confidence": confidence, "Roc_confidence": roc_confidence,
                                 "list_program_types": unique_list_programs})
                        else:
                            if (program_pred == 2 or program_pred == 1):
                                drugUse = serializer.validated_data.get('drug_Use')
                                ylsSUBAB = serializer.validated_data.get('yls_Subab_Score')
                                alcholUSe = serializer.validated_data.get('alcohol_Use')
                                p13_model = pickle.load(open(
                                    os.path.join(SOURCE_DIR, "new_pickles","R_LR_P13_11march.sav"),
                                    "rb"))
                                p13_model_preds = p13_model.predict(Xtest)
                                if (drugUse == 0 and ylsSUBAB == 0 and alcholUSe == 0):
                                    condition_program = 3
                                    query6 = Adelphoi_Mapping.objects.filter(program=condition_program,
                                                                             gender=serializer.validated_data.get(
                                                                                 'gender'),
                                                                             level_of_care=level_pred,
                                                                             facility_type=facility_preds)
                                    for i in query6:
                                        program_list.append(i.program_name)
                                        level_list.append(i.level_names)
                                        facility_names.append(i.facility_names)
                                        # program_type.append(i.program_type)
                                        program_model_suggested_list.append(i.program_model_suggested)
                                    for i in program_model_suggested_list:
                                        if i not in unique_program_model_suggested_list:
                                            unique_program_model_suggested_list.append(i)
                                    query_default = Adelphoi_Mapping.objects.filter(
                                        program_model_suggested=program_model_suggested_list[0],
                                        default_level_facility=True)
                                    level_default = []
                                    facility_default = []
                                    for i in query_default:
                                        level_default.append(i.level_of_care)
                                        facility_default.append(i.facility_type)
                                    confidence = \
                                    program_condition(
                                        condition_program, level_default[0],
                                        facility_default[0])[0]
                                    roc_confidence = \
                                    program_condition(
                                        condition_program, level_default[0],
                                        facility_default[0])[1]
                                    serializer.save(
                                        roc_confidence=roc_confidence,
                                        program=condition_program,
                                        confidence=confidence,
                                        family_support=data[
                                            'Family support'][0],
                                        level_of_aggression=data[
                                            'Level of aggression'][0],
                                        fire_setting=data['Fire setting'][0],
                                        client_self_harm=data[
                                            'Client self-harm'][0],
                                        cans_LifeFunctioning=data[
                                            'CANS_LifeFunctioning'][0],
                                        cans_YouthStrengths=data[
                                            'CANS_YouthStrengths'][0],
                                        cans_CareGiverStrengths=data[
                                            'CANS_CareGiverStrengths'][0],
                                        cans_Culture=data['CANS_Culture'][0],
                                        cans_YouthBehavior=data[
                                            'CANS_YouthBehavior'][0],
                                        cans_YouthRisk=data[
                                            'CANS_YouthRisk'][0],
                                        cans_Trauma_Exp=data[
                                            'CANS_Trauma_Exp'][0],
                                        yls_PriorCurrentOffenses_Score=
                                        data[
                                        'YLS_PriorCurrentOffenses_Score'][0],
                                        yls_FamCircumstances_Score=data[
                                            'YLS_FamCircumstances_Score'][0],
                                        yls_Edu_Employ_Score=data[
                                            'YLS_Edu_Employ_Score'][0],
                                        yls_Peer_Score=data[
                                            'YLS_Peer_Score'][0],
                                        yls_Subab_Score=data[
                                            'YLS_Subab_Score'][0],
                                        yls_Leisure_Score=data[
                                            'YLS_Leisure_Score'][0],
                                        yls_Personality_Score=data[
                                            'YLS_Personality_Score'][0],
                                        yls_Attitude_Score=data[
                                            'YLS_Attitude_Score'][0],
                                        Screening_tool_Trauma=
                                        data['Screening tool for Trauma--Total score'][0],
                                        FAST_FamilyTogetherScore=data[
                                            'FAST_FamilyTogetherScore'][0],
                                        FAST_CaregiverAdvocacyScore=data[
                                            'FAST_CaregiverAdvocacyScore'][0],
                                        inclusionary_criteria=serializer.validated_data.get(
                                            'inclusionary_criteria'),
                                        model_program=program_model_suggested_list[0]
                                    )
                                    return JsonResponse(
                                        {"model program": int(program_pred[0]),
                                         "program": int(p13_model_preds),
                                         "Level of care": int(level_pred[0]),
                                         "program_type":
                                             unique_program_model_suggested_list,
                                         # program_model_suggested_list,
                                         "Facility Type":
                                             int(facility_preds[0]),
                                         "gender": int(
                                             serializer.validated_data.get(
                                             'gender')),
                                         "Confidence": confidence,
                                         "Roc_confidence": roc_confidence,
                                         "list_program_types":
                                             unique_list_programs
                                         })
                                else:
                                    query4 = Adelphoi_Mapping.objects.filter(
                                        program=p13_model_preds,
                                        gender=serializer.validated_data.get(
                                            'gender'),
                                        level_of_care=level_pred,
                                        facility_type=facility_preds
                                    )
                                    for i in query4:
                                        program_list.append(i.program_name)
                                        level_list.append(i.level_names)
                                        facility_names.append(
                                            i.facility_names)
                                        # program_type.append(i.program_type)
                                        program_model_suggested_list.append(
                                            i.program_model_suggested)
                                    for i in program_model_suggested_list:
                                        if i not in unique_program_model_suggested_list:
                                            unique_program_model_suggested_list.append(i)
                                    query_default = Adelphoi_Mapping.objects.filter(
                                        program_model_suggested=
                                        program_model_suggested_list[0],
                                        default_level_facility=True)
                                    level_default = []
                                    facility_default = []
                                    for i in query_default:
                                        level_default.append(i.level_of_care)
                                        facility_default.append(
                                            i.facility_type)
                                    confidence =program_condition(
                                        p13_model_preds, level_default[0],
                                        facility_default[0])[0]
                                    roc_confidence =program_condition(
                                        p13_model_preds, level_default[0],
                                        facility_default[0])[1]
                                    serializer.save(
                                        roc_confidence=roc_confidence,
                                        program=p13_model_preds,
                                        confidence=confidence,
                                        family_support=data[
                                            'Family support'][0],
                                        level_of_aggression=data[
                                            'Level of aggression'][0],
                                        fire_setting=data['Fire setting'][0],
                                        client_self_harm=data[
                                            'Client self-harm'][0],
                                        cans_LifeFunctioning=data[
                                            'CANS_LifeFunctioning'][0],
                                        cans_YouthStrengths=data[
                                            'CANS_YouthStrengths'][0],
                                        cans_CareGiverStrengths=data[
                                            'CANS_CareGiverStrengths'][0],
                                        cans_Culture=data['CANS_Culture'][0],
                                        cans_YouthBehavior=data[
                                            'CANS_YouthBehavior'][0],
                                        cans_YouthRisk=data[
                                            'CANS_YouthRisk'][0],
                                        cans_Trauma_Exp=data[
                                            'CANS_Trauma_Exp'][0],
                                        yls_PriorCurrentOffenses_Score=data[
                                        'YLS_PriorCurrentOffenses_Score'][0],
                                        yls_FamCircumstances_Score=data[
                                            'YLS_FamCircumstances_Score'][0],
                                        yls_Edu_Employ_Score=data[
                                            'YLS_Edu_Employ_Score'][0],
                                        yls_Peer_Score=data[
                                            'YLS_Peer_Score'][0],
                                        yls_Subab_Score=data[
                                            'YLS_Subab_Score'][0],
                                        yls_Leisure_Score=data[
                                            'YLS_Leisure_Score'][0],
                                        yls_Personality_Score=data[
                                            'YLS_Personality_Score'][0],
                                        yls_Attitude_Score=data[
                                            'YLS_Attitude_Score'][0],
                                        Screening_tool_Trauma=
                                        data['Screening tool for Trauma--Total score'][0],
                                        FAST_FamilyTogetherScore=data[
                                            'FAST_FamilyTogetherScore'][0],
                                        FAST_CaregiverAdvocacyScore=data[
                                            'FAST_CaregiverAdvocacyScore'][0],
                                        inclusionary_criteria=serializer.validated_data.get(
                                            'inclusionary_criteria'),
                                        model_program=program_model_suggested_list[0]
                                    )

                                    return JsonResponse(
                                        {"model program": int(program_pred[0]),
                                         "program": int(p13_model_preds),
                                         "Level of care": int(level_pred[0]),
                                         "program_type":
                                             unique_program_model_suggested_list,
                                         # program_model_suggested_list,
                                         "Facility Type": int(facility_preds[0]),
                                         "gender": int(
                                             serializer.validated_data.get('gender')),
                                         "Confidence": confidence,
                                         "Roc_confidence": roc_confidence,
                                         "list_program_types":
                                             unique_list_programs
                                         })
                            else:
                                query5 = Adelphoi_Mapping.objects.filter(
                                    program=program_pred,
                                    gender=serializer.validated_data.get('gender'),
                                    level_of_care=level_pred,
                                    facility_type=facility_preds)
                                # logger.info(
                                #     'where Exclusionary_Criteria-False, gender-1,inclusionary_criteria=false,program_pred-(1,3)')
                                for i in query5:
                                    program_num.append(i.program)
                                    program_list.append(i.program_name)
                                    level_list.append(i.level_names)
                                    facility_names.append(i.facility_names)
                                    #
                                    program_model_suggested_list.append(
                                        i.program_model_suggested)
                                for i in program_model_suggested_list:
                                    if i not in unique_program_model_suggested_list:
                                        unique_program_model_suggested_list.append(i)
                                query_default = Adelphoi_Mapping.objects.filter(
                                    program_model_suggested=program_model_suggested_list[0],
                                    default_level_facility=True)
                                level_default = []
                                facility_default = []
                                for i in query_default:
                                    level_default.append(i.level_of_care)
                                    facility_default.append(i.facility_type)
                                confidence = program_condition(
                                    program_pred, level_default[0], facility_default[0])[0]
                                roc_confidence = program_condition(
                                    program_pred, level_default[0],
                                    facility_default[0])[1]
                                serializer.save(
                                    roc_confidence=roc_confidence,
                                    program=program_num[0],
                                    confidence=confidence,
                                    family_support=data['Family support'][0],
                                    level_of_aggression=data[
                                        'Level of aggression'][0],
                                    fire_setting=data['Fire setting'][0],
                                    client_self_harm=data['Client self-harm'][0],
                                    cans_LifeFunctioning=data[
                                        'CANS_LifeFunctioning'][0],
                                    cans_YouthStrengths=data[
                                        'CANS_YouthStrengths'][0],
                                    cans_CareGiverStrengths=data[
                                        'CANS_CareGiverStrengths'][0],
                                    cans_Culture=data['CANS_Culture'][0],
                                    cans_YouthBehavior=data['CANS_YouthBehavior'][0],
                                    cans_YouthRisk=data['CANS_YouthRisk'][0],
                                    cans_Trauma_Exp=data['CANS_Trauma_Exp'][0],
                                    yls_PriorCurrentOffenses_Score=data[
                                        'YLS_PriorCurrentOffenses_Score'][0],
                                    yls_FamCircumstances_Score=data[
                                        'YLS_FamCircumstances_Score'][0],
                                    yls_Edu_Employ_Score=data[
                                        'YLS_Edu_Employ_Score'][0],
                                    yls_Peer_Score=data['YLS_Peer_Score'][0],
                                    yls_Subab_Score=data[
                                        'YLS_Subab_Score'][0],
                                    yls_Leisure_Score=data[
                                        'YLS_Leisure_Score'][0],
                                    yls_Personality_Score=data[
                                        'YLS_Personality_Score'][0],
                                    yls_Attitude_Score=data[
                                        'YLS_Attitude_Score'][0],
                                    Screening_tool_Trauma=data[
                                     'Screening tool for Trauma--Total score'][0],
                                    FAST_FamilyTogetherScore=data[
                                        'FAST_FamilyTogetherScore'][0],
                                    FAST_CaregiverAdvocacyScore=data[
                                        'FAST_CaregiverAdvocacyScore'][0],
                                    inclusionary_criteria=serializer.validated_data.get(
                                        'inclusionary_criteria'),
                                    model_program=program_model_suggested_list[0]
                                )
                                return JsonResponse(
                                    {"model program": int(program_pred[0]),
                                     "program": int(program_pred[0]),
                                     "Level of care": int(level_pred[0]),
                                     "program_type": unique_program_model_suggested_list,
                                     "Facility Type": int(facility_preds[0]),
                                     "gender": int(serializer.validated_data.get('gender')),
                                     "Confidence": confidence,
                                     "Roc_confidence": roc_confidence,
                                     "list_program_types": unique_list_programs
                                     })
                else:
                    if serializer.validated_data.get('gender') == 1:
                        condition_program = 3
                        # logger.info('where exit loop gender-1')
                        query6 = Adelphoi_Mapping.objects.filter(
                            program=condition_program,
                            gender=serializer.validated_data.get('gender'),
                            level_of_care=level_pred,
                            facility_type=facility_preds)
                        for i in query6:
                            program_num.append(i.program)
                            program_list.append(i.program_name)
                            level_list.append(i.level_names)
                            facility_names.append(i.facility_names)
                            program_model_suggested_list.append(
                                i.program_model_suggested)
                        for i in program_model_suggested_list:
                            if i not in unique_program_model_suggested_list:
                                unique_program_model_suggested_list.append(i)
                        query_default = Adelphoi_Mapping.objects.filter(
                            program_model_suggested=program_model_suggested_list[0],
                            default_level_facility=True)
                        level_default = []
                        facility_default = []
                        for i in query_default:
                            level_default.append(i.level_of_care)
                            facility_default.append(i.facility_type)
                        confidence = program_condition(
                            condition_program,
                            level_default[0], facility_default[0])[0]
                        roc_confidence = program_condition(
                            condition_program,
                            level_default[0], facility_default[0])[1]
                        serializer.save(
                            roc_confidence=roc_confidence,
                            program=program_num[0],
                            condition_program=condition_program,
                            confidence=confidence,
                            family_support=data['Family support'][0],
                            level_of_aggression=data['Level of aggression'][0],
                            fire_setting=data['Fire setting'][0],
                            client_self_harm=data['Client self-harm'][0],
                            cans_LifeFunctioning=data[
                                'CANS_LifeFunctioning'][0],
                            cans_YouthStrengths=data[
                                'CANS_YouthStrengths'][0],
                            cans_CareGiverStrengths=data[
                                'CANS_CareGiverStrengths'][0],
                            cans_Culture=data['CANS_Culture'][0],
                            cans_YouthBehavior=data[
                                'CANS_YouthBehavior'][0],
                            cans_YouthRisk=data['CANS_YouthRisk'][0],
                            cans_Trauma_Exp=data['CANS_Trauma_Exp'][0],
                            yls_PriorCurrentOffenses_Score=data[
                                'YLS_PriorCurrentOffenses_Score'][0],
                            yls_FamCircumstances_Score=data[
                                'YLS_FamCircumstances_Score'][0],
                            yls_Edu_Employ_Score=data[
                                'YLS_Edu_Employ_Score'][0],
                            yls_Peer_Score=data['YLS_Peer_Score'][0],
                            yls_Subab_Score=data['YLS_Subab_Score'][0],
                            yls_Leisure_Score=data['YLS_Leisure_Score'][0],
                            yls_Personality_Score=data[
                                'YLS_Personality_Score'][0],
                            yls_Attitude_Score=data['YLS_Attitude_Score'][0],
                            Screening_tool_Trauma=
                            data['Screening tool for Trauma--Total score'][0],
                            FAST_FamilyTogetherScore=data[
                                'FAST_FamilyTogetherScore'][0],
                            FAST_CaregiverAdvocacyScore=data[
                                'FAST_CaregiverAdvocacyScore'][0],
                            inclusionary_criteria=serializer.validated_data.get(
                                'inclusionary_criteria'),
                            model_program=program_model_suggested_list[0]
                        )
                        return JsonResponse(
                            {"model program": int(program_pred[0]),
                             "program": int(condition_program),
                             "Level of care": int(level_pred[0]),
                             "program_type": unique_program_model_suggested_list,
                             # program_model_suggested_list,
                             "Facility Type": int(facility_preds[0]),
                             "gender": int(
                                 serializer.validated_data.get('gender')),
                             "Confidence": confidence,
                             "Roc_confidence": roc_confidence,
                             "list_program_types": unique_list_programs})
            else:
                serializer.save()
                return JsonResponse({"Result": "Thank you for registering with ADELPHOI"})
            return JsonResponse({"data": "Failure"})
        else:
            return JsonResponse({"data": "serializer not allowed"})
    else:
        return JsonResponse({"data": "method not allowed"})
