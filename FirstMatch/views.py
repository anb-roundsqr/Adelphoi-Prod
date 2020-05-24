# Create your views here.
import os
import json
from django.http import JsonResponse
from rest_framework.generics import (
    ListCreateAPIView, UpdateAPIView, RetrieveUpdateAPIView,
    ListAPIView, RetrieveAPIView
)
from .models import (
    ModelTests, Adelphoi_Mapping, ProgramModel, ModelLocation,
    FacilityModel, LevelModel, ReferralSource
)
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import pickle
from rest_framework.response import Response
from .serializers import (
    ModelTestsSerializers, ProgramLocationSerialzer, ProgramLevelSerialzer,
    AdminInterface, FilterSerialzer, Adelphoi_placementSerializer,
    Adelphoi_referredSerializer, ProgramIndSerializer, ProgramSerializer,
    LocationSerializer, LocationIndSerializer, Available_programSerializer,
    Program_PCRSerializer, ReferralIndSerializer, refferalSerializer
)

from django_filters.rest_framework import DjangoFilterBackend
from AdelphoiProject.settings import SOURCE_DIR

from django_filters import rest_framework as filters
import logging

logging.basicConfig(
    filename='test_log.log',
    level=logging.INFO,
    filemode='a',
    format='%(asctime)s %(process)d-%(name)-12s'
           ' %(levelname)-8s -%(funcName)s  -  %(lineno)d     %(message)s'
)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AdelphoiList(ListCreateAPIView):
    serializer_class = ModelTestsSerializers
    queryset = ModelTests.objects.all()

    def get(self, request):
        logger.info('get method for AdelphoiList')
        return Response("Success")

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query_gender = Adelphoi_Mapping.objects.filter(
            gender=serializer.validated_data.get('gender')
        )  # ,program_model_suggested = serializer.validated_data.get(
        # "program_model_suggested")
        suggested_programs = []
        unique_list_programs = []
        if query_gender.count() > 0:
            for i in query_gender:
                suggested_programs.append(
                    i.program_model_suggested
                )  # program_type
            for i in suggested_programs:
                if i not in unique_list_programs:
                    unique_list_programs.append(i)

        if not serializer.validated_data.get('Exclusionary_Criteria'):
            logger.info(
                'AdelphoiList class where Exclusionary_Criteria is False'
            )
            dt = {
                'Gender': serializer.validated_data.get('gender'),
                'AgeAtEnrollStart': serializer.validated_data.get(
                    'ageAtEnrollStart'
                ),
                'CYF_code': serializer.validated_data.get('CYF_code'),
                'LS_Type': serializer.validated_data.get('ls_type'),
                'EpisodeNumber': serializer.validated_data.get(
                    'episode_number'
                ),
                'RefSourceName': serializer.validated_data.get(
                    'RefSourceCode'
                ),
                'Number of foster care placements':
                    serializer.validated_data.get(
                        'number_of_foster_care_placements'
                    ),
                'AgeAtEpisodeStart': serializer.validated_data.get(
                    'ageAtEpisodeStart'
                ),
                'Number of prior placements \n'
                '(excluding shelter and detention)':
                    serializer.validated_data.get(
                        'number_of_prior_placements'
                    ),
                'Number of prior treatment terminations'
                ' (excluding shelter or detention)':
                    serializer.validated_data.get(
                        'number_of_prior_treatment_terminations'
                    ),
                'Length of time since living at home':
                    serializer.validated_data.get(
                        'length_of_time_since_living_at_home'
                    ),
                'Termination directly to AV': serializer.validated_data.get(
                    'termination_directly_to_AV'
                ),
                'Death Caregiver': serializer.validated_data.get(
                    'death_Caregiver'
                ),
                'Borderline IQ (below 70)': serializer.validated_data.get(
                    'borderline_IQ'
                ),
                'Hist of prior program SAO': serializer.validated_data.get(
                    'hist_of_prior_program_SAO'
                ),
                'Death Silblings': serializer.validated_data.get(
                    'death_Silblings'
                ),
                'Alcohol Use': serializer.validated_data.get('alcohol_Use'),
                'Drug Use': serializer.validated_data.get('drug_Use'),
                'Incarcerated caregivers': serializer.validated_data.get(
                    'incarcerated_caregivers'
                ),
                'Incarcerated siblings': serializer.validated_data.get(
                    'incarcerated_siblings'
                ),
                'Number of prior AWOLS': serializer.validated_data.get(
                    'number_of_prior_AWOLS'
                ),
                'Animal cruelty': serializer.validated_data.get(
                    'animal_cruelty'
                ),
                'Number of prior hospitalizations':
                    serializer.validated_data.get('prior_hospitalizations'),
                'Compliant with medication': serializer.validated_data.get(
                    'compliant_with_meds'
                ),
                'Significant mental health symptoms':
                    serializer.validated_data.get(
                        'significant_mental_health_symptoms'
                    ),
                'Severe mental health symptoms':
                    serializer.validated_data.get(
                        'severe_mental_health_symptoms'
                    ),
                'Autism Diagnosis': serializer.validated_data.get(
                    'autism_Diagnosis'
                ),
                'Borderline Personality': serializer.validated_data.get(
                    'borderline_Personality'
                ),
                'Psychosis': serializer.validated_data.get('psychosis'),
                'Reactive Attachment Disorder': serializer.validated_data.get(
                    'reactive_Attachment_Disorder'
                ),
                'Schizophrenia': serializer.validated_data.get(
                    'schizophrenia'
                ),
                'YLS_PriorCurrentOffenses_Score':
                    serializer.validated_data.get(
                        'yls_PriorCurrentOffenses_Score'
                    ),
                'YLS_FamCircumstances_Score': serializer.validated_data.get(
                    'yls_FamCircumstances_Score'
                ),
                'YLS_Edu_Employ_Score': serializer.validated_data.get(
                    'yls_Edu_Employ_Score'
                ),
                'YLS_Peer_Score': serializer.validated_data.get(
                    'yls_Peer_Score'
                ),
                'YLS_Subab_Score': serializer.validated_data.get(
                    'yls_Subab_Score'
                ),
                'YLS_Leisure_Score': serializer.validated_data.get(
                    'yls_Leisure_Score'
                ),
                'YLS_Personality_Score': serializer.validated_data.get(
                    'yls_Personality_Score'
                ),
                'YLS_Attitude_Score': serializer.validated_data.get(
                    'yls_Attitude_Score'
                ),
                'Client self-harm': serializer.validated_data.get(
                    'client_self_harm'
                ),

                'CANS_LifeFunctioning': serializer.validated_data.get(
                    'cans_LifeFunctioning'
                ),
                'CANS_YouthStrengths': serializer.validated_data.get(
                    'cans_YouthStrengths'
                ),
                'CANS_CareGiverStrengths': serializer.validated_data.get(
                    'cans_CareGiverStrengths'
                ),
                'CANS_Culture': serializer.validated_data.get('cans_Culture'),
                'CANS_YouthBehavior': serializer.validated_data.get(
                    'cans_YouthBehavior'
                ),
                'CANS_YouthRisk': serializer.validated_data.get(
                    'cans_YouthRisk'
                ),
                'CANS_Trauma_Exp': serializer.validated_data.get(
                    'cans_Trauma_Exp'
                ),

                'Family support': serializer.validated_data.get(
                    'family_support'
                ),
                'Level of aggression': serializer.validated_data.get(
                    'level_of_aggression'
                ),
                'Fire setting': serializer.validated_data.get('fire_setting'),
                'Abuse, or neglect': serializer.validated_data.get(
                    'abuse_neglect'
                ),
                'Screening tool for Trauma--Total score':
                    serializer.validated_data.get('Screening_tool_Trauma'),
                'FAST_FamilyTogetherScore': serializer.validated_data.get(
                    'FAST_FamilyTogetherScore'
                ),
                'FAST_CaregiverAdvocacyScore': serializer.validated_data.get(
                    'FAST_CaregiverAdvocacyScore'
                )
            }  #
            logger.info("values are %s", dt)
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
                    data['CANS_CareGiverStrengths'] = 10.0757  # 10.129032
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
                    data['FAST_CaregiverAdvocacyScore'] = 6.5319  # 6.674419
                else:
                    data['FAST_CaregiverAdvocacyScore'] = 6.0120  # 5.887500
            if data['YLS_PriorCurrentOffenses_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data[
                        'YLS_PriorCurrentOffenses_Score'
                    ] = 0.6750  # 0.684211
                else:
                    data[
                        'YLS_PriorCurrentOffenses_Score'
                    ] = 0.5913  # 0.566667
            if data['YLS_FamCircumstances_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data['YLS_FamCircumstances_Score'] = 3.7631  # 3.750000
                else:
                    data['YLS_FamCircumstances_Score'] = 2.7956  # 2.811111
            if data['YLS_Edu_Employ_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data['YLS_Edu_Employ_Score'] = 3.0789  # 2.944444
                else:
                    data['YLS_Edu_Employ_Score'] = 2.3655  # 2.322222
            if data['YLS_Peer_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data['YLS_Peer_Score'] = 2.8947  # 2.833333
                else:
                    data['YLS_Peer_Score'] = 1.9462  # 1.944444
            if data['YLS_Subab_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data['YLS_Subab_Score'] = 2.1578  # 2.166667
                else:
                    data['YLS_Subab_Score'] = 1.301  # 1.311111
            if data['YLS_Leisure_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data['YLS_Leisure_Score'] = 1.943  # 1.944444
                else:
                    data['YLS_Leisure_Score'] = 2.00  # 2.000000
            if data['YLS_Personality_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data['YLS_Personality_Score'] = 3.5789  # 3.555556
                else:
                    data['YLS_Personality_Score'] = 3.1935  # 3.188889
            if data['YLS_Attitude_Score'][0] is None:
                if data['Gender'][0] == 1:
                    data['YLS_Attitude_Score'] = 1.8947  # 1.944444
                else:
                    data['YLS_Attitude_Score'] = 1.3978  # 1.377778
            if data['Screening tool for Trauma--Total score'][0] is None:
                if data['Gender'][0] == 1:
                    data[
                        'Screening tool for Trauma--Total score'
                    ] = 14.7555  # 14.595238
                else:
                    data[
                        'Screening tool for Trauma--Total score'
                    ] = 14.7244  # 14.634409

            data['LS_Type'].fillna(data['LS_Type'].mode()[0], inplace=True)
            data['LS_Type'] = data['LS_Type'].astype('int')

            dummies = pd.DataFrame()
            for column in ['Gender', 'LS_Type',
                           'CYF_code']:  # ,'RefSourceName'
                dummies1 = pd.get_dummies(data[column], prefix=column)
                dummies[dummies1.columns] = dummies1.copy(deep=False)

            cols = [
                'Gender_1', 'Gender_2', 'LS_Type_1', 'LS_Type_2',
                'LS_Type_3', 'LS_Type_4', 'LS_Type_5', 'CYF_code_0',
                'CYF_code_1', 'CYF_code_2'
                ]
            # 'RefSourceName_1', 'RefSourceName_2', 'RefSourceName_3',
            # 'RefSourceName_4', 'RefSourceName_5', 'RefSourceName_6',
            # 'RefSourceName_7', 'RefSourceName_8', 'RefSourceName_9',
            # 'RefSourceName_10', 'RefSourceName_11', 'RefSourceName_12',
            # 'RefSourceName_13', 'RefSourceName_14', 'RefSourceName_15',
            # 'RefSourceName_16', 'RefSourceName_17', 'RefSourceName_18',
            # 'RefSourceName_19', 'RefSourceName_20', 'RefSourceName_21',
            # 'RefSourceName_22', 'RefSourceName_23', 'RefSourceName_24',
            # 'RefSourceName_25', 'RefSourceName_26', 'RefSourceName_27',
            # 'RefSourceName_28', 'RefSourceName_29', 'RefSourceName_30',
            # 'RefSourceName_31', 'RefSourceName_32', 'RefSourceName_34',
            # 'RefSourceName_35', 'RefSourceName_36', 'RefSourceName_37',
            # 'RefSourceName_38', 'RefSourceName_39', 'RefSourceName_40',
            # 'RefSourceName_41', 'RefSourceName_42', 'RefSourceName_43',
            # 'RefSourceName_44', 'RefSourceName_45', 'RefSourceName_46',
            # 'RefSourceName_47', 'RefSourceName_48', 'RefSourceName_49',
            # 'RefSourceName_50', 'RefSourceName_51', 'RefSourceName_52',
            # 'RefSourceName_53', 'RefSourceName_54', 'RefSourceName_55',
            # 'RefSourceName_56', 'RefSourceName_57', 'RefSourceName_59',
            # 'RefSourceName_60'
            for col in cols:
                if col in dummies.columns:
                    print('present', col)
                else:
                    dummies[col] = 0
            data.fillna(0, inplace=True)
            numeric_cols = [
                'Gender', 'LS_Type', 'CYF_code', 'RefSourceName',
                'EpisodeNumber', 'Number of foster care placements',
                'AgeAtEpisodeStart', 'Number of prior placements'
                                     ' \n(excluding shelter and detention)',
                'AgeAtEnrollStart', 'Number of prior treatment terminations'
                                    ' (excluding shelter or detention)',
                'Length of time since living at home',
                'Termination directly to AV', 'Death Caregiver',
                'Borderline IQ (below 70)', 'Hist of prior program SAO',
                'Death Silblings', 'Alcohol Use', 'Drug Use',
                'Incarcerated caregivers', 'Incarcerated siblings',
                'Number of prior AWOLS', 'Animal cruelty',
                'Number of prior hospitalizations',
                'Compliant with medication',
                'Significant mental health symptoms',
                'Severe mental health symptoms', 'Autism Diagnosis',
                'Borderline Personality', 'Psychosis',
                'Reactive Attachment Disorder', 'Schizophrenia'
            ]

            # converting float to integer
            for col in numeric_cols:
                data[col] = pd.to_numeric(
                    data[col],
                    errors='coerce',
                    downcast='integer'
                )
            ###
            Feature_names = [
                'EpisodeNumber', 'Number of foster care placements',
                'AgeAtEpisodeStart', 'Number of prior placements'
                                     ' \n(excluding shelter and detention)',
                'Number of prior treatment terminations'
                ' (excluding shelter or detention)',
                'Length of time since living at home',
                'Termination directly to AV', 'Death Caregiver',
                'Borderline IQ (below 70)', 'Hist of prior program SAO',
                'Death Silblings', 'Alcohol Use', 'Drug Use',
                'Incarcerated caregivers', 'Incarcerated siblings',
                'Number of prior AWOLS', 'Animal cruelty',
                'Number of prior hospitalizations',
                'Compliant with medication',
                'Significant mental health symptoms',
                'Severe mental health symptoms',
                'Autism Diagnosis', 'Borderline Personality', 'Psychosis',
                'Reactive Attachment Disorder', 'Schizophrenia',
                'YLS_PriorCurrentOffenses_Score',
                'YLS_FamCircumstances_Score',
                'YLS_Edu_Employ_Score', 'YLS_Peer_Score', 'YLS_Subab_Score',
                'YLS_Leisure_Score', 'YLS_Personality_Score',
                'YLS_Attitude_Score', 'Client self-harm',
                'CANS_LifeFunctioning', 'CANS_YouthStrengths',
                'CANS_CareGiverStrengths', 'CANS_Culture',
                'CANS_YouthBehavior', 'CANS_YouthRisk', 'CANS_Trauma_Exp',
                'Family support', 'Level of aggression', 'Fire setting',
                'Abuse, or neglect', 'Screening tool for Trauma--Total score'
            ]

            Xtest = pd.DataFrame(data[Feature_names])
            Xtest[dummies.columns] = dummies
            #  ### server####
            # level_model = pickle.load(
            #     open(
            #         "/home/ubuntu/Adelphoi/adelphoi-django/sources/"
            #         "LR_LC_13feb.sav",
            #         "rb"
            #     )
            # )
            # program_model = pickle.load(
            #     open(
            #         "/home/ubuntu/Adelphoi/adelphoi-django/sources/"
            #         "DT_P_13feb.sav",
            #         "rb"
            #     )
            # )
            # facility_model = pickle.load(
            #     open(
            #         "/home/ubuntu/Adelphoi/adelphoi-django/sources/"
            #         "LR_FT_13feb.sav",
            #         "rb"
            #     )
            # )
            # PC_model = pickle.load(
            #     open(
            #         "/home/ubuntu/Adelphoi/adelphoi-django/sources/"
            #         "LR_PC_13feb.sav",
            #         "rb"
            #     )
            # )
            # #################

            level_model = pickle.load(
                open(
                    os.path.join(SOURCE_DIR, "new_pickles", "R_LR_LC_11march.sav"),
                    "rb"
                )
            )
            program_model = pickle.load(
                open(
                    os.path.join(SOURCE_DIR, "new_pickles", "R_DT_P_11march.sav"),
                    "rb"
                )
            )
            facility_model = pickle.load(
                open(
                    os.path.join(SOURCE_DIR, "new_pickles", "R_LR_FT_11march.sav"),
                    "rb"
                )
            )
            PC_model = pickle.load(
                open(
                    os.path.join(SOURCE_DIR, "new_pickles", "R_LR_PC_11march.sav"),
                    "rb"
                )
            )
            level_pred = level_model.predict(Xtest)
            program_pred = program_model.predict(Xtest)
            facility_preds = facility_model.predict(Xtest)
            query = Adelphoi_Mapping.objects.filter(
                program=program_pred,
                gender=serializer.validated_data.get('gender'),
                level_of_care=level_pred,
                facility_type=facility_preds
            )

            def program_condition(condition_program,
                                  level_pred, facility_preds):
                logger.info('program_condition function')
                Xp = pd.DataFrame(
                    data[
                        [
                            'EpisodeNumber',
                            'Number of foster care placements',
                            'AgeAtEpisodeStart',
                            'Number of prior placements'
                            ' \n(excluding shelter and detention)',
                            'Number of prior treatment terminations'
                            ' (excluding shelter or detention)',
                            'Length of time since living at home',
                            'Termination directly to AV',
                            'Death Caregiver', 'Borderline IQ (below 70)',
                            'Hist of prior program SAO', 'Death Silblings',
                            'Alcohol Use', 'Drug Use',
                            'Incarcerated caregivers', 'Incarcerated siblings',
                            'Number of prior AWOLS', 'Animal cruelty',
                            'Number of prior hospitalizations',
                            'Compliant with medication',
                            'Significant mental health symptoms',
                            'Severe mental health symptoms',
                            'Autism Diagnosis', 'Borderline Personality',
                            'Psychosis', 'Reactive Attachment Disorder',
                            'Schizophrenia'
                        ]
                    ]
                )

                Xp['Program'] = condition_program
                Xp['Level_of_Care'] = level_pred
                Xp['FacilityType'] = facility_preds
                Xp[dummies.columns] = dummies
                PC_proba = PC_model.predict_proba(Xp)
                if PC_proba[0][1] > (0.5):
                    Xp['ProgramCompletion'] = 1
                else:
                    Xp['ProgramCompletion'] = 0
                roc_model = pickle.load(
                    open(
                        os.path.join(
                            SOURCE_DIR,
                            "new_pickles",
                            "R_LR_RC_11march.sav"
                        ),
                        "rb"
                    )
                )
                roc_result = roc_model.predict_proba(Xp)
                return [
                    round(PC_proba[0][1] * 100),
                    round(roc_result[0][1] * 100)
                ]

            program_list = []
            level_list = []
            facility_names = []
            # program_type = []
            program_num = []
            program_model_suggested_list = []
            if query.count() > 0:
                if serializer.validated_data.get('gender') == 1:
                    logger.info(
                        'where Exclusionary_Criteria-False,'
                        ' gender-1(Female),condition_program-3'
                    )
                    condition_program = 3
                    query2 = Adelphoi_Mapping.objects.filter(
                        program=condition_program,
                        gender=serializer.validated_data.get('gender'),
                        level_of_care=level_pred,
                        facility_type=facility_preds
                    )

                    for i in query2:
                        program_num.append(i.program)
                        program_list.append(i.program_name)
                        level_list.append(i.level_names)
                        facility_names.append(i.facility_names)
                        program_model_suggested_list.append(
                            i.program_model_suggested
                        )
                        # program_type.append(i.program_type)
                    query_default = Adelphoi_Mapping.objects.filter(
                        program_model_suggested=program_model_suggested_list[
                            0],
                        default_level_facility=True)
                    level_default = []
                    facility_default = []
                    for i in query_default:
                        level_default.append(i.level_of_care)
                        facility_default.append(i.facility_type)
                    confidence = program_condition(
                        condition_program,
                        level_default[0],
                        facility_default[0]
                    )[0]
                    roc_confidence = program_condition(
                        condition_program,
                        level_default[0],
                        facility_default[0]
                    )[1]
                    serializer.save(
                        facility_type=facility_preds,
                        level_of_care=level_pred,
                        model_pred= program_pred,
                        roc_confidence=roc_confidence,
                        program=program_num[0],
                        condition_program=condition_program,
                        confidence=confidence,
                        family_support=data['Family support'][0],
                        level_of_aggression=data['Level of aggression'][0],
                        fire_setting=data['Fire setting'][0],
                        client_self_harm=data['Client self-harm'][0],
                        cans_LifeFunctioning=data['CANS_LifeFunctioning'][0],
                        cans_YouthStrengths=data['CANS_YouthStrengths'][0],
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
                        yls_Edu_Employ_Score=data['YLS_Edu_Employ_Score'][0],
                        yls_Peer_Score=data['YLS_Peer_Score'][0],
                        yls_Subab_Score=data['YLS_Subab_Score'][0],
                        yls_Leisure_Score=data['YLS_Leisure_Score'][0],
                        yls_Personality_Score=data[
                            'YLS_Personality_Score'][0],
                        yls_Attitude_Score=data['YLS_Attitude_Score'][0],
                        Screening_tool_Trauma=data[
                            'Screening tool for Trauma--Total score'][0],
                        FAST_FamilyTogetherScore=data[
                            'FAST_FamilyTogetherScore'][0],
                        FAST_CaregiverAdvocacyScore=data[
                            'FAST_CaregiverAdvocacyScore'][0],
                        inclusionary_criteria=serializer.validated_data.get(
                            'inclusionary_criteria'
                        ),
                        model_program=program_model_suggested_list[0]
                    )  # confidence = PC_proba[0][1]*100

                    return Response(
                        {
                            "model program": program_pred,
                            "program": condition_program,
                            "Level of care": level_pred,
                            "program_type": program_model_suggested_list,
                            "Facility Type": facility_preds,
                            "gender": serializer.validated_data.get('gender'),
                            "Confidence": confidence,
                            "Roc_confidence": roc_confidence,
                            "list_program_types": unique_list_programs
                         }
                    )
                else:
                    if serializer.validated_data.get('inclusionary_criteria'):
                        logger.info(
                            'where Exclusionary_Criteria-False,'
                            ' gender-2(male),'
                            ' inclusionary_criteria=true,'
                            'condition_program-2'
                        )
                        condition_program = 2
                        query3 = Adelphoi_Mapping.objects.filter(
                            program=condition_program,
                            gender=serializer.validated_data.get('gender'),
                            level_of_care=level_pred,
                            facility_type=facility_preds
                        )
                        for i in query3:
                            program_num.append(i.program)
                            program_list.append(i.program_name)
                            level_list.append(i.level_names)
                            facility_names.append(i.facility_names)
                            # program_type.append(i.program_type)
                            program_model_suggested_list.append(
                                i.program_model_suggested)
                        query_default = Adelphoi_Mapping.objects.filter(
                            program_model_suggested=program_model_suggested_list[0],
                            default_level_facility=True
                        )
                        level_default = []
                        facility_default = []
                        for i in query_default:
                            level_default.append(i.level_of_care)
                            facility_default.append(i.facility_type)
                        confidence = program_condition(
                            condition_program,
                            level_default[0],
                            facility_default[0]
                        )[0]
                        roc_confidence = program_condition(
                            condition_program,
                            level_default[0],
                            facility_default[0]
                        )[1]
                        serializer.save(
                            facility_type=facility_preds,
                            level_of_care=level_pred,
                            model_pred=program_pred,
                            roc_confidence=roc_confidence,
                            program=program_num[0],
                            condition_program=condition_program,
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
                            yls_Subab_Score=data['YLS_Subab_Score'][0],
                            yls_Leisure_Score=data['YLS_Leisure_Score'][0],
                            yls_Personality_Score=data[
                                'YLS_Personality_Score'][0],
                            yls_Attitude_Score=data['YLS_Attitude_Score'][0],
                            Screening_tool_Trauma=data[
                                'Screening tool for Trauma--Total score'][0],
                            FAST_FamilyTogetherScore=data[
                                'FAST_FamilyTogetherScore'][0],
                            FAST_CaregiverAdvocacyScore=data[
                                'FAST_CaregiverAdvocacyScore'][0],
                            inclusionary_criteria=serializer.validated_data.get(
                                'inclusionary_criteria'
                            ),
                            model_program=program_model_suggested_list[0]
                        )
                        return Response(
                            {
                                "model program": program_pred,
                                "program": condition_program,
                                "Level of care": level_pred,
                                "program_type": program_model_suggested_list,
                                "Facility Type": facility_preds,
                                "gender": serializer.validated_data.get(
                                    'gender'),
                                "Confidence": confidence,
                                "Roc_confidence": roc_confidence,
                                "list_program_types": unique_list_programs
                            }
                        )
                    else:
                        if program_pred == 2:
                            drugUse = serializer.validated_data.get(
                                'drug_Use')
                            ylsSUBAB = serializer.validated_data.get(
                                'yls_Subab_Score')
                            alcholUSe = serializer.validated_data.get(
                                'alcohol_Use')
                            logger.info(
                                'where Exclusionary_Criteria-False,'
                                ' gender-2(male),'
                                'inclusionary_criteria=false,'
                                'program_pred-2'
                            )
                            # #server
                            # p13_model = pickle.load(
                            #     open(
                            #         "/home/ubuntu/Adelphoi/adelphoi-django/"
                            #          "sources/LR_P13_13feb.sav", "rb"
                            #     )
                            # )
                            p13_model = pickle.load(
                                open(
                                    os.path.join(
                                        SOURCE_DIR,
                                        "new_pickles",
                                        "R_LR_P13_11march.sav"
                                    ),
                                    "rb"
                                )
                            )
                            p13_model_preds = p13_model.predict(Xtest)
                            if drugUse == 0 and ylsSUBAB == 0 and \
                                    alcholUSe == 0:
                                condition_program = 3
                                query6 = Adelphoi_Mapping.objects.filter(
                                    program=condition_program,
                                    gender=serializer.validated_data.get(
                                        'gender'),
                                    level_of_care=level_pred,
                                    facility_type=facility_preds
                                )
                                for i in query6:
                                    program_list.append(i.program_name)
                                    level_list.append(i.level_names)
                                    facility_names.append(i.facility_names)
                                    # program_type.append(i.program_type)
                                    program_model_suggested_list.append(
                                        i.program_model_suggested)
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
                                    level_default[0],
                                    facility_default[0]
                                )[0]
                                roc_confidence = program_condition(
                                    condition_program,
                                    level_default[0],
                                    facility_default[0]
                                )[1]
                                serializer.save(
                                    facility_type=facility_preds,
                                    level_of_care=level_pred,
                                    model_pred=program_pred,
                                    roc_confidence=roc_confidence,
                                    program=condition_program,
                                    confidence=confidence,
                                    family_support=data['Family support'][0],
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
                                    cans_YouthRisk=data['CANS_YouthRisk'][0],
                                    cans_Trauma_Exp=data[
                                        'CANS_Trauma_Exp'][0],
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
                                        'Screening tool for '
                                        'Trauma--Total score'
                                    ][0],
                                    FAST_FamilyTogetherScore=data[
                                        'FAST_FamilyTogetherScore'][0],
                                    FAST_CaregiverAdvocacyScore=data[
                                        'FAST_CaregiverAdvocacyScore'][0],
                                    inclusionary_criteria=serializer.validated_data.get(
                                        'inclusionary_criteria'
                                    ),
                                    model_program=program_model_suggested_list[
                                        0]
                                )
                                return Response(
                                    {
                                        "model program": program_pred,
                                        "program": condition_program,
                                        "Level of care": level_pred,
                                        "program_type":
                                            program_model_suggested_list,
                                        "Facility Type": facility_preds,
                                        "gender":
                                            serializer.validated_data.get(
                                                'gender'),
                                        "Confidence": confidence,
                                        "Roc_confidence": roc_confidence,
                                        "list_program_types":
                                            unique_list_programs
                                    }
                                )
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
                                    facility_names.append(i.facility_names)
                                    # program_type.append(i.program_type)
                                    program_model_suggested_list.append(
                                        i.program_model_suggested)
                                query_default = Adelphoi_Mapping.objects.filter(
                                    program_model_suggested=program_model_suggested_list[0],
                                    default_level_facility=True
                                )
                                level_default = []
                                facility_default = []
                                for i in query_default:
                                    level_default.append(i.level_of_care)
                                    facility_default.append(i.facility_type)
                                confidence = program_condition(
                                    p13_model_preds,
                                    level_default[0],
                                    facility_default[0]
                                )[0]
                                roc_confidence = program_condition(
                                    p13_model_preds,
                                    level_default[0],
                                    facility_default[0]
                                )[1]
                                serializer.save(
                                    facility_type=facility_preds,
                                    level_of_care=level_pred,
                                    model_pred=program_pred,
                                    roc_confidence=roc_confidence,
                                    program=p13_model_preds,
                                    confidence=confidence,
                                    family_support=data['Family support'][0],
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
                                    cans_YouthRisk=data['CANS_YouthRisk'][0],
                                    cans_Trauma_Exp=data[
                                        'CANS_Trauma_Exp'][0],
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
                                        'Screening tool for'
                                        ' Trauma--Total score'
                                    ][0],
                                    FAST_FamilyTogetherScore=data[
                                        'FAST_FamilyTogetherScore'][0],
                                    FAST_CaregiverAdvocacyScore=data[
                                        'FAST_CaregiverAdvocacyScore'][0],
                                    inclusionary_criteria=serializer.validated_data.get(
                                        'inclusionary_criteria'
                                    ),
                                    model_program=program_model_suggested_list[0]
                                )
                                return Response(
                                    {
                                        "model program": program_pred,
                                        "program": p13_model_preds,
                                        "Level of care": level_pred,
                                        "program_type":
                                            program_model_suggested_list,
                                        "Facility Type": facility_preds,
                                        "gender":
                                            serializer.validated_data.get(
                                                'gender'),
                                        "Confidence": confidence,
                                        "Roc_confidence": roc_confidence,
                                        "list_program_types":
                                            unique_list_programs
                                    }
                                )
                        else:
                            # if program_pred == 2 :
                            drugUse = serializer.validated_data.get(
                                'drug_Use')
                            ylsSUBAB = serializer.validated_data.get(
                                'yls_Subab_Score')
                            alcholUSe = serializer.validated_data.get(
                                'alcohol_Use')
                            logger.info(
                                'where Exclusionary_Criteria-False,'
                                ' gender-2(male),'
                                'inclusionary_criteria=false,'
                                'program_pred-1 0r 3'
                            )
                            # #server
                            # p13_model = pickle.load(
                            #     open(
                            #         "/home/ubuntu/Adelphoi/adelphoi-django/"
                            #          "sources/LR_P13_13feb.sav", "rb"
                            #     )
                            # )
                            p13_model = pickle.load(
                                open(
                                    os.path.join(
                                        SOURCE_DIR,
                                        "new_pickles",
                                        "R_LR_P13_11march.sav"
                                    ),
                                    "rb"
                                )
                            )
                            p13_model_preds = p13_model.predict(Xtest)
                            if drugUse == 0 and ylsSUBAB == 0 and \
                                    alcholUSe == 0:
                                condition_program = 3
                                query6 = Adelphoi_Mapping.objects.filter(
                                    program=condition_program,
                                    gender=serializer.validated_data.get(
                                        'gender'),
                                    level_of_care=level_pred,
                                    facility_type=facility_preds
                                )
                                for i in query6:
                                    program_list.append(i.program_name)
                                    level_list.append(i.level_names)
                                    facility_names.append(i.facility_names)
                                    # program_type.append(i.program_type)
                                    program_model_suggested_list.append(
                                        i.program_model_suggested)
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
                                    level_default[0],
                                    facility_default[0]
                                )[0]
                                roc_confidence = program_condition(
                                    condition_program,
                                    level_default[0],
                                    facility_default[0]
                                )[1]
                                serializer.save(
                                    facility_type=facility_preds,
                                    level_of_care=level_pred,
                                    model_pred=program_pred,
                                    roc_confidence=roc_confidence,
                                    program=condition_program,
                                    confidence=confidence,
                                    family_support=data['Family support'][0],
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
                                    cans_YouthRisk=data['CANS_YouthRisk'][0],
                                    cans_Trauma_Exp=data[
                                        'CANS_Trauma_Exp'][0],
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
                                        'Screening tool for '
                                        'Trauma--Total score'
                                    ][0],
                                    FAST_FamilyTogetherScore=data[
                                        'FAST_FamilyTogetherScore'][0],
                                    FAST_CaregiverAdvocacyScore=data[
                                        'FAST_CaregiverAdvocacyScore'][0],
                                    inclusionary_criteria=serializer.validated_data.get(
                                        'inclusionary_criteria'
                                    ),
                                    model_program=program_model_suggested_list[
                                        0]
                                )
                                return Response(
                                    {
                                        "model program": program_pred,
                                        "program": condition_program,
                                        "Level of care": level_pred,
                                        "program_type":
                                            program_model_suggested_list,
                                        "Facility Type": facility_preds,
                                        "gender":
                                            serializer.validated_data.get(
                                                'gender'),
                                        "Confidence": confidence,
                                        "Roc_confidence": roc_confidence,
                                        "list_program_types":
                                            unique_list_programs
                                    }
                                )
                            else:
                                query5 = Adelphoi_Mapping.objects.filter(
                                    program=program_pred,
                                    gender=serializer.validated_data.get('gender'),
                                    level_of_care=level_pred,
                                    facility_type=facility_preds
                                )
                                for i in query5:
                                    program_list.append(i.program_name)
                                    level_list.append(i.level_names)
                                    facility_names.append(i.facility_names)
                                    # program_type.append(i.program_type)
                                    program_model_suggested_list.append(
                                        i.program_model_suggested)
                                query_default = Adelphoi_Mapping.objects.filter(
                                    program_model_suggested=program_model_suggested_list[0],
                                    default_level_facility=True
                                )
                                level_default = []
                                facility_default = []
                                for i in query_default:
                                    level_default.append(i.level_of_care)
                                    facility_default.append(i.facility_type)
                                confidence = program_condition(
                                    program_pred,
                                    level_default[0],
                                    facility_default[0]
                                )[0]
                                roc_confidence = program_condition(
                                    program_pred,
                                    level_default[0],
                                    facility_default[0]
                                )[1]
                                serializer.save(
                                    facility_type=facility_preds,
                                    level_of_care=level_pred,
                                    model_pred=program_pred,
                                    roc_confidence=roc_confidence,
                                    program=program_pred,
                                    confidence=confidence,
                                    family_support=data['Family support'][0],
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
                                    cans_YouthRisk=data['CANS_YouthRisk'][0],
                                    cans_Trauma_Exp=data[
                                        'CANS_Trauma_Exp'][0],
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
                                        'Screening tool for'
                                        ' Trauma--Total score'
                                    ][0],
                                    FAST_FamilyTogetherScore=data[
                                        'FAST_FamilyTogetherScore'][0],
                                    FAST_CaregiverAdvocacyScore=data[
                                        'FAST_CaregiverAdvocacyScore'][0],
                                    inclusionary_criteria=serializer.validated_data.get(
                                        'inclusionary_criteria'
                                    ),
                                    model_program=program_model_suggested_list[0]
                                )
                                return Response(
                                    {
                                        "model program": program_pred,
                                        "program": program_pred,
                                        "Level of care": level_pred,
                                        "program_type":
                                            program_model_suggested_list,
                                        "Facility Type": facility_preds,
                                        "gender":
                                            serializer.validated_data.get(
                                                'gender'),
                                        "Confidence": confidence,
                                        "Roc_confidence": roc_confidence,
                                        "list_program_types":
                                            unique_list_programs
                                    }
                                )
            else:
                if serializer.validated_data.get('gender') == 1:
                    condition_program = 3
                    logger.info('where exit loop gender-1')
                    query6 = Adelphoi_Mapping.objects.filter(
                        program=condition_program,
                        gender=serializer.validated_data.get('gender'),
                        level_of_care=level_pred,
                        facility_type=facility_preds
                    )
                    for i in query6:
                        program_num.append(i.program)
                        program_list.append(i.program_name)
                        level_list.append(i.level_names)
                        facility_names.append(i.facility_names)
                        #
                        program_model_suggested_list.append(
                            i.program_model_suggested)
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
                        level_default[0],
                        facility_default[0]
                    )[0]
                    roc_confidence = program_condition(
                        condition_program,
                        level_default[0],
                        facility_default[0]
                    )[1]
                    serializer.save(
                        facility_type=facility_preds,
                        level_of_care=level_pred,model_pred= program_pred,
                        roc_confidence=roc_confidence, program=program_num[0],
                        condition_program=condition_program,
                        confidence=confidence,
                        family_support=data['Family support'][0],
                        level_of_aggression=data['Level of aggression'][0],
                        fire_setting=data['Fire setting'][0],
                        client_self_harm=data['Client self-harm'][0],
                        cans_LifeFunctioning=data['CANS_LifeFunctioning'][0],
                        cans_YouthStrengths=data['CANS_YouthStrengths'][0],
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
                        yls_Edu_Employ_Score=data['YLS_Edu_Employ_Score'][0],
                        yls_Peer_Score=data['YLS_Peer_Score'][0],
                        yls_Subab_Score=data['YLS_Subab_Score'][0],
                        yls_Leisure_Score=data['YLS_Leisure_Score'][0],
                        yls_Personality_Score=data[
                            'YLS_Personality_Score'][0],
                        yls_Attitude_Score=data['YLS_Attitude_Score'][0],
                        Screening_tool_Trauma=data[
                            'Screening tool for Trauma--Total score'][0],
                        FAST_FamilyTogetherScore=data[
                            'FAST_FamilyTogetherScore'][0],
                        FAST_CaregiverAdvocacyScore=data[
                            'FAST_CaregiverAdvocacyScore'][0],
                        inclusionary_criteria=serializer.validated_data.get(
                            'inclusionary_criteria'),
                        model_program=program_model_suggested_list[0])
                    return Response({
                        "model program": program_pred,
                        "program": condition_program,
                        "Level of care": level_pred,
                        "program_type": program_model_suggested_list,
                        "Facility Type": facility_preds,
                        "gender": serializer.validated_data.get(
                            'gender'),
                        "Confidence": confidence,
                        "Roc_confidence": roc_confidence,
                        "list_program_types": unique_list_programs
                    })
        else:
            serializer.save()
            return Response({"Result": "Thank you for registering with ADELPHOI"})
        return Response({"data": "Failure"})


class Adelphoi_placement(RetrieveAPIView):
    serializer_class = Adelphoi_placementSerializer
    queryset = ModelTests.objects.all()


class AdelphoiSubmission(RetrieveUpdateAPIView):  # UpdateAPIView

    serializer_class = ProgramLevelSerialzer
    # ModelTestsSerializers_selected_program,
    # ModelTestsSerializer_program_model_suggested
    queryset = ModelTests.objects.all()

    def put(self, request, *args, **kwargs):
        mt: ModelTests = ModelTests.objects.filter(
            client_code=kwargs['pk']
        )[0]

        logger.info('Using AdelphoiSubmission function ')
        suggested_programs2 = request.GET['suggested_programs']
        # location = request.GET['location_names']

        query = Adelphoi_Mapping.objects.filter(
            gender=mt.gender
        )
        # ,program_model_suggested = serializer.validated_data.get(
        #     "program_model_suggested"
        # )
        suggested_programs = []
        suggested_location = []
        location_names = []

        selected_program = []
        selected_level = []
        selected_facility = []
        if query.count() > 0:
            for i in query:
                suggested_programs.append(i.program_model_suggested)
                suggested_location.append(i.location_names)

            query_location = Adelphoi_Mapping.objects.filter(
                program_model_suggested=suggested_programs2
            )
            for q in query_location:
                location_names.append(q.location_names)
                selected_program.append(q.program)
                selected_level.append(q.level_of_care)
                selected_facility.append(q.facility_type)
        data = {"suggested_programs": suggested_programs,
                "location_names": suggested_location}

        mt.client_selected_level = int(selected_level[0])
        mt.client_selected_facility = int(selected_facility[0])
        mt.client_selected_program = int(selected_program[0])
        mt.save()

        return Response({"data": data})

    def get(self, request, *args, **kwargs):
        mt: ModelTests = ModelTests.objects.filter(
            client_code=kwargs['pk'])[0]
        # (mt.program)
        query = Adelphoi_Mapping.objects.filter(gender=mt.gender)
        suggested_programs = []
        locatin_name = []
        for i in query:
            suggested_programs.append(i.program_model_suggested)
            locatin_name.append(i.location_names)
        data = {"suggested_programs": suggested_programs}
        return Response(data)


class Adelphoi_program(ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            mt: ModelTests = ModelTests.objects.filter(
                client_code=kwargs['pk'])[0]
            logger.info('Adelphoi_program--program search')
            selected_program = mt.client_selected_program
            selected_location = mt.client_selected_locations
            query_gender = Adelphoi_Mapping.objects.filter(
                gender=mt.gender)
            # ,program_model_suggested = serializer.validated_data.get(
            #     "program_model_suggested"
            # )
            suggested_programs = []
            unique_list_programs = []
            if query_gender.count() > 0:
                for i in query_gender:
                    suggested_programs.append(i.program_model_suggested)
                for i in suggested_programs:
                    if i not in unique_list_programs:
                        unique_list_programs.append(i)
                data = {
                    'program_model_suggested': unique_list_programs,
                    'selected_program': selected_program,
                    'selected_location': selected_location
                }
                return Response(data)
            else:
                return Response({"result": "Client not exists"})
        except Exception:
            return Response({"result": "failure"})


class Adelphoi_referredprogram(UpdateAPIView):
    serializer_class = Adelphoi_referredSerializer
    queryset = ModelTests.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mt: ModelTests = ModelTests.objects.filter(
            client_code=kwargs['pk']).first()
        if mt:
            logger.info('Adelphoi_referredprogram--Update programs')
            mt.referred_program = serializer.validated_data.get(
                'referred_program')
            mt.save()
            return Response({"data": "success"})
        else:
            return Response({"result": "client not exists"})


class Adelphoi_location(ListAPIView):
    def get(self, request, *args, **kwargs):
        referred_program = request.GET['referred_program']
        mt: ModelTests = ModelTests.objects.filter(client_code=kwargs['pk'])

        if mt.exists():
            logger.info('Adelphoi_location--List of locations')
            gender_list = []
            for i in mt:
                gender_list.append(i.gender)
            query = Adelphoi_Mapping.objects.filter(
                program_model_suggested=referred_program,gender=gender_list[0]
            )  # program_name=referred_program, gender=gender_list[0]
            suggested_location = []
            new_suggested_locations = []
            if query.count() > 0:
                for i in query:
                    if i not in suggested_location:
                        suggested_location.append(i.location_names)
                appended_locations = sum(suggested_location, [])
                for i in appended_locations:
                    if i not in new_suggested_locations:
                        new_suggested_locations.append(i)
            else:
                logger.info('Adelphoi_location --query not exists')
                return Response({"result": "NO MATCHES FOUND"})
            return Response({
                'Suggested Locations': new_suggested_locations
            })
        else:
            logger.info('Adelphoi_location--clientCode not exists')
            return Response({"result": "client not exists"})


class AdelphoiResult(UpdateAPIView):  # UpdateAPIView

    serializer_class = ProgramLocationSerialzer
    queryset = ModelTests.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mt: ModelTests = ModelTests.objects.filter(
            client_code=kwargs['pk']).first()
        if mt:
            client_selected_program = serializer.validated_data.get(
                'client_selected_program')
            # request.GET['client_selected_program']
            client_selected_location = serializer.validated_data.get(
                'client_selected_locations')
            # request.GET['client_selected_location']
            location_names = []
            selected_program = []
            selected_level = []
            selected_facility = []
            query_location = Adelphoi_Mapping.objects.filter(
                program_model_suggested=client_selected_program
            )
            if query_location.count() > 0:
                for q in query_location:
                    location_names.append(q.location_names)
                    selected_program.append(q.program)
                    selected_level.append(q.level_of_care)
                    selected_facility.append(q.facility_type)
            else:
                return Response({"Response": "not found"})
            mt.client_selected_level = int(selected_level[0])
            mt.client_selected_facility = int(selected_facility[0])
            mt.client_selected_program = client_selected_program
            mt.client_selected_locations = client_selected_location
            mt.save()
            logger.info(
                'AdelphoiResult---client_selected_level,'
                'client_selected_facility,'
                'client_selected_program & client_selected_locations saved')
            return Response({"result": "values are inserted"})
        else:
            logger.info('AdelphoiResult---ClientCode not exists')
            return Response({"result": "client not exists"})


class ProgramCompletionLevel(RetrieveUpdateAPIView):  # UpdateAPIView
    serializer_class = ProgramLevelSerialzer
    queryset = ModelTests.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mt: ModelTests = ModelTests.objects.filter(
            client_code=kwargs['pk']).first()
        if mt:
            mt.Program_Completion = serializer.validated_data.get(
                'Program_Completion')
            mt.Returned_to_Care = serializer.validated_data.get(
                'Returned_to_Care')
            mt.program_significantly_modified = serializer.validated_data.get(
                'program_significantly_modified')
            logger.info(
                'ProgramCompletionLevel---Program_Completion,'
                'Returned_to_Care is saved')
            mt.save()
            return Response({"data": "success"})
        else:
            logger.info('ProgramCompletionLevel---ClientCode not exists')
            return Response({"result": "client not exists"})


class AdminUpdate(ListCreateAPIView):
    serializer_class = AdminInterface
    queryset = Adelphoi_Mapping.objects.all()

    def post(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # raise_exception=True
        serializer.save()

        return Response({"data": "okay"})


class SearchFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = ModelTests
        fields = ['client_code', 'name']


# To search results based on client_code or name
class ClientList(ListAPIView):
    queryset = ModelTests.objects.all()
    serializer_class = FilterSerialzer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client_code', 'name']
    filterset_class = SearchFilter


class LocationMapping(UpdateAPIView):
    serializer_class = LocationSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mt: ModelTests = ModelTests.objects.filter(client_code=kwargs['pk'])
        if mt.exists():
            mt.client_selected_locations = serializer.validated_data.get(
                'client_selected_locations')
            mt.save()
            logger.info(
                'Location_Mapping---client_selected_locations are saving')
            return Response({"data": "success"})
        else:
            logger.info('Location_Mapping--Client code not exists')
            return Response({"result": "client not exists"})


# to save adelphoi mapping values from admin
@csrf_exempt
def saveData(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        #
        program = data['program']
        program_name = data['program_name']
        gender = data['gender']
        gender_name = data['gender_name']
        level_of_care = data['level_of_care']
        level_names = data['level_names']

        location = data['location']
        location_names = data['location_names']

        facility_type = data['facility_type']
        facility_names = data['facility_names']
        program_model_suggested = data['program_model_suggested']
        program_type = data['program_type']

        Adelphoi_Mapping(
            location=list(eval(location)),
            location_names=location_names.split(','),
            program=program,
            program_name=program_name,
            gender=gender,
            gender_name=gender_name,
            level_of_care=level_of_care,
            level_names=level_names,
            facility_type=facility_type,
            facility_names=facility_names,
            program_model_suggested=program_model_suggested,
            program_type=program_type
        ).save()
        logger.info('saveData---Mapping values are stored')
        return JsonResponse({"data": "Data inserted successfully"})
    else:
        logger.info('saveData--Get method not allowed')
        return JsonResponse({"data", "Method not allowed"})


# to add program
@csrf_exempt
def programSave(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            program_name = data['program_name']
            ProgramModel(
                program_name=program_name,
                program=ProgramModel.objects.count() + 1
            ).save()  # ,program = ProgramModel.objects.count() + 1
            result = ProgramModel.objects.filter(program_name=program_name)[0]
            program_id = result.program
            logger.info('programSave---Program saved based on id')
            return JsonResponse({"program_id": program_id, "Sucess": "true"})
        except Exception:
            logger.info('programSave---Program id error')
            return JsonResponse({"error": "no matches found"})
    else:
        logger.info('programSave---Method not alloed')
        return JsonResponse({"result": "Method not exist"})


# to get programs list
class Program_list(ListAPIView):
    serializer_class = ProgramIndSerializer
    queryset = ProgramModel.objects.all()


# to program modify
class ProgramModify(RetrieveUpdateAPIView):
    serializer_class = ProgramSerializer
    queryset = ProgramModel.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            ProgramModel.objects.filter(program=kwargs['pk']).delete()
            return Response({"result": 'deleted'})
        except Exception:
            return Response({"result": 'no program id found'})

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data.get('program_name')
        mt: ProgramModel = ProgramModel.objects.filter(
            program=kwargs['pk']).first()
        mt.program_name = result
        mt.save()
        Adelphoi_Mapping.objects.filter(program=kwargs['pk']).update(
            program_name=result)
        logger.info('ProgramModify--Program name change')
        return Response({"program_id": mt.program,
                         "Result": "Program name is modified"})


#
#
# # to get Referral list
# class referral_list(ListAPIView):
#     serializer_class = ProgramIndSerializer
#     queryset = ReferralModel.objects.all()
#
#


# to daa locations to list
@csrf_exempt
def locationSave(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            location_names = data['location_name']
            ModelLocation(
                location_names=location_names,
                location=ModelLocation.objects.count() + 1
            ).save()  # ,program = ProgramModel.objects.count() + 1
            result = ModelLocation.objects.filter(
                location_names=location_names)[0]
            location = result.location
            logger.info('loactionSave ---locations saved based on id')
            return JsonResponse({"location_id": location, "Sucess": "true"})
        except Exception:
            logger.info('loactionSave---error location Id')
            return JsonResponse({"error": "no matches found"})
    else:
        logger.info('loactionSave---method not allowed')
        return JsonResponse({"result": "Method not exist"})


# to get Location list
class Location_list(ListAPIView):
    serializer_class = LocationIndSerializer
    queryset = ModelLocation.objects.all()


# to location modify

class LocationModify(RetrieveUpdateAPIView):
    serializer_class = LocationSerializer
    queryset = ModelLocation.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            ModelLocation.objects.filter(location=kwargs['pk']).delete()
            return Response({"result": 'deleted'})
        except Exception:
            return Response({"result": 'no location id found'})

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mt: ModelLocation = ModelLocation.objects.filter(
            location=kwargs['pk']).first()
        mt.location_names = serializer.validated_data.get('location_names')
        mt.save()
        logger.info('LocationModify---locations modify')
        return Response({"Result": "location name is modified"})


@csrf_exempt
def dataSave(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        program = data['program']
        location = data['location']
        gender = data['gender']
        facility_type = data['facility_type']
        level_of_care = data['level_of_care']
        program_model_suggested = data['program_model_suggested']
        program_type = data['program_type']

        location_names = []
        try:
            query1 = ProgramModel.objects.filter(program=program)[0]
            program_name = query1.program_name
            for i in location:
                result = ModelLocation.objects.filter(location=i)[0]
                location_names.append(result.location_names)
            if gender == 1:
                gender_name = "Female"
            else:
                gender_name = "Male"
            facility_query = FacilityModel.objects.filter(
                facility_type=facility_type)[0]
            facility_names = facility_query.facility_names
            level_of_query = LevelModel.objects.filter(
                level_of_care=level_of_care)[0]
            level_names = level_of_query.level_names

            Adelphoi_Mapping(
                program=program, program_name=program_name, gender=gender,
                location=location, location_names=location_names,
                gender_name=gender_name, facility_names=facility_names,
                level_names=level_names, facility_type=facility_type,
                level_of_care=level_of_care,
                program_model_suggested=program_model_suggested,
                program_type=program_type
            ).save()

            logger.info('dataSave ---Mappings are saved')
            return JsonResponse({"data": "Data inserted successfully"})

        except Exception:
            logger.info('dataSave---error in program/location/gender')
            return JsonResponse({"result": "program name not exists"})
        return JsonResponse({"data": "Data inserted successfully"})
    else:
        logger.info('dataSave--method not allowed')
        return JsonResponse({"data", "Method not allowed"})


class AvailablePrograms(ListAPIView):
    serializer_class = Available_programSerializer
    queryset = ProgramModel.objects.all()


class RecommndedProgramPCR(UpdateAPIView):
    serializer_class = Program_PCRSerializer  # ProgramSerialzer
    queryset = ModelTests.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            mt: ModelTests = ModelTests.objects.filter(
                client_code=kwargs['pk'])[0]
            client_selected_program = serializer.validated_data.get(
                'client_selected_program')

            query_loc_facility = Adelphoi_Mapping.objects.filter(
                gender=mt.gender,
                program_model_suggested=client_selected_program,
                default_level_facility=True
            )

            level_of_care_values = []
            facility_values = []
            program_value = []
            for i in query_loc_facility:
                level_of_care_values.append(i.level_of_care)
                facility_values.append(i.facility_type)
                program_value.append(i.program)
            level_pred = level_of_care_values[0]
            facility_preds = facility_values[0]
            condition_program = program_value[0]

            if condition_program > 3:
                result = 0
                return Response({"pcr": result, "roc_confidence": result})
            else:

                dt = {
                    'EpisodeNumber': mt.episode_number,
                    'Number of foster care placements':
                        mt.number_of_foster_care_placements,
                    'AgeAtEpisodeStart': mt.ageAtEpisodeStart,
                    'Number of prior placements'
                    ' \n(excluding shelter and detention)':
                        mt.number_of_prior_placements,
                    'Number of prior treatment terminations'
                    ' (excluding shelter or detention)':
                        mt.number_of_prior_treatment_terminations,
                    'Length of time since living at home':
                        mt.length_of_time_since_living_at_home,
                    'Termination directly to AV':
                        mt.termination_directly_to_AV,
                    'Death Caregiver': mt.death_Caregiver,
                    'Borderline IQ (below 70)': mt.borderline_IQ,
                    'Hist of prior program SAO': mt.hist_of_prior_program_SAO,
                    'Death Silblings': mt.death_Silblings,
                    'Alcohol Use': mt.alcohol_Use, 'Drug Use': mt.drug_Use,
                    'Incarcerated caregivers': mt.incarcerated_caregivers,
                    'Incarcerated siblings': mt.incarcerated_siblings,
                    'Number of prior AWOLS': mt.number_of_prior_AWOLS,
                    'Animal cruelty': mt.animal_cruelty,
                    'Number of prior hospitalizations':
                        mt.prior_hospitalizations,
                    'Compliant with medication': mt.compliant_with_meds,
                    'Significant mental health symptoms':
                        mt.significant_mental_health_symptoms,
                    'Severe mental health symptoms':
                        mt.severe_mental_health_symptoms,
                    'Autism Diagnosis': mt.autism_Diagnosis,
                    'Borderline Personality': mt.borderline_Personality,
                    'Psychosis': mt.psychosis,
                    'Reactive Attachment Disorder':
                        mt.reactive_Attachment_Disorder,
                    'Schizophrenia': mt.schizophrenia,
                    'Gender': mt.gender, 'LS_Type': mt.ls_type,
                    'CYF_code': mt.CYF_code
                }

                data = pd.DataFrame(dt, index=[0])

                dummies = pd.DataFrame()
                for column in ['Gender', 'LS_Type',
                               'CYF_code']:  # , 'RefSourceName'
                    dummies1 = pd.get_dummies(data[column], prefix=column)
                    dummies[dummies1.columns] = dummies1.copy(deep=False)

                cols = [
                    'Gender_1', 'Gender_2', 'LS_Type_1', 'LS_Type_2',
                    'LS_Type_3', 'LS_Type_4', 'LS_Type_5',
                    'CYF_code_0', 'CYF_code_1', 'CYF_code_2'
                ]
                # , 'RefSourceName_1', 'RefSourceName_2', 'RefSourceName_3',
                # 'RefSourceName_4', 'RefSourceName_5', 'RefSourceName_6',
                # 'RefSourceName_7', 'RefSourceName_8', 'RefSourceName_9',
                # 'RefSourceName_10', 'RefSourceName_11', 'RefSourceName_12',
                # 'RefSourceName_13', 'RefSourceName_14', 'RefSourceName_15',
                # 'RefSourceName_16', 'RefSourceName_17', 'RefSourceName_18',
                # 'RefSourceName_19', 'RefSourceName_20', 'RefSourceName_21',
                # 'RefSourceName_22', 'RefSourceName_23', 'RefSourceName_24',
                # 'RefSourceName_25', 'RefSourceName_26', 'RefSourceName_27',
                # 'RefSourceName_28', 'RefSourceName_29', 'RefSourceName_30',
                # 'RefSourceName_31', 'RefSourceName_32', 'RefSourceName_34',
                # 'RefSourceName_35', 'RefSourceName_36', 'RefSourceName_37',
                # 'RefSourceName_38', 'RefSourceName_39', 'RefSourceName_40',
                # 'RefSourceName_41', 'RefSourceName_42', 'RefSourceName_43',
                # 'RefSourceName_44', 'RefSourceName_45', 'RefSourceName_46',
                # 'RefSourceName_47', 'RefSourceName_48', 'RefSourceName_49',
                # 'RefSourceName_50', 'RefSourceName_51', 'RefSourceName_52',
                # 'RefSourceName_53', 'RefSourceName_54', 'RefSourceName_55',
                # 'RefSourceName_56', 'RefSourceName_57', 'RefSourceName_59',
                # 'RefSourceName_60'
                for col in cols:
                    if col in dummies.columns:
                        print('present', col)
                    else:
                        dummies[col] = 0
                # server
                # PC_model = pickle.load(
                #     open(
                #         "/home/ubuntu/Adelphoi/adelphoi-django/sources/"
                #         "LR_PC_13feb.sav",
                #         "rb"
                #     )
                # )
                PC_model = pickle.load(
                    open(
                        os.path.join(
                            SOURCE_DIR,
                            "new_pickles",
                            "R_LR_PC_11march.sav",
                        ),
                        "rb"
                    )
                )

                Xp = pd.DataFrame(
                    data[
                        [
                            'EpisodeNumber',
                            'Number of foster care placements',
                            'AgeAtEpisodeStart',
                            'Number of prior placements'
                            ' \n(excluding shelter and detention)',
                            'Number of prior treatment terminations'
                            ' (excluding shelter or detention)',
                            'Length of time since living at home',
                            'Termination directly to AV',
                            'Death Caregiver', 'Borderline IQ (below 70)',
                            'Hist of prior program SAO', 'Death Silblings',
                            'Alcohol Use', 'Drug Use',
                            'Incarcerated caregivers',
                            'Incarcerated siblings', 'Number of prior AWOLS',
                            'Animal cruelty',
                            'Number of prior hospitalizations',
                            'Compliant with medication',
                            'Significant mental health symptoms',
                            'Severe mental health symptoms',
                            'Autism Diagnosis', 'Borderline Personality',
                            'Psychosis', 'Reactive Attachment Disorder',
                            'Schizophrenia'
                        ]]
                )
                Xp['Program'] = condition_program
                Xp['Level_of_Care'] = level_pred
                Xp['FacilityType'] = facility_preds
                Xp[dummies.columns] = dummies
                PC_proba = PC_model.predict_proba(Xp)
                if PC_proba[0][1] > (0.5):
                    Xp['ProgramCompletion'] = 1
                else:
                    Xp['ProgramCompletion'] = 0
                roc_model = pickle.load(
                    open(
                        os.path.join(
                            SOURCE_DIR,
                            "new_pickles",
                            "R_LR_RC_11march.sav"
                        ),
                        "rb"
                    )
                )
                roc_result = roc_model.predict_proba(Xp)
                result = round(PC_proba[0][1] * 100)
                roc_results = round(roc_result[0][1]*100)
                mt.confidence = result
                mt.roc_confidence = roc_results
                mt.save()
                # serializer.save(confidence=result)
                # serializer.save(
                #     condition_program=condition_program,
                #     confidence=result
                # )
                return Response({
                    "pcr": result,
                    "roc_confidence": roc_results
                })
        except Exception:
            return Response({"result": "No combinations found!!"})


# to get programs list
class Refferal_list(ListAPIView):
    serializer_class = ReferralIndSerializer
    queryset = ReferralSource.objects.all()


# to add referralSources
@csrf_exempt
def referralSave(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            referral_name = data['referral_name']
            # print(
            #     ReferralSource.objects.filter(
            #         referral_name=referral_name
            #     )
            # )
            ReferralSource(
                referral_name=referral_name,
                referral_code=ReferralSource.objects.count() + 1,
                id=ReferralSource.objects.count() + 1
            ).save()
            result = ReferralSource.objects.filter(
                referral_name=referral_name)[0]
            rf_code = result.referral_code
            logger.info('referralSave---referral saved based on id')
            return JsonResponse({
                "referral_code": rf_code,
                "Sucess": "true"
            })  # "referral_code": rf_code,
        except Exception:
            logger.info('referralSave---Referral id error')
            return JsonResponse({"error": "no matches found"})
    else:
        logger.info('programSave---Method not alloed')
        return JsonResponse({"result": "Method not exist"})


# to referral modify
class referralModify(RetrieveUpdateAPIView):
    serializer_class = refferalSerializer
    queryset = ReferralSource.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            ReferralSource.objects.filter(
                referral_code=kwargs['pk']
            ).delete()
            return Response({"result": 'deleted'})
        except Exception:
            return Response({"result": 'no program id found'})

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data.get('referral_name')
        mt: ReferralSource = ReferralSource.objects.filter(
            referral_code=kwargs['pk']
        ).first()
        mt.referral_name = result
        mt.save()
        ReferralSource.objects.filter(
            referral_code=kwargs['pk']
        ).update(referral_name=result)
        logger.info('referralModify--Referral name change')
        return Response(
            {
                "referral_id": mt.referral_code,
                "Result": "Referral name is modified"
            }
        )
