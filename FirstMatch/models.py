from djongo import models
from django import forms
# from datetime import datetime
# from django.urls import reverse
# from django_better_admin_arrayfield.models.fields import ArrayField
# Create your models here.
# from django.contrib.postgres.fields import ArrayField
# from jsonfield import JSONField


class ModelTests(models.Model):

    GENDER_CHOICES = (
        (1, 'Female'),
        (2, "Male")
    )
    # RACE_CHOICES = ((1, 'caucasian'),
    #                 (2, 'African American'),
    #                 (3, 'Hispanic'),
    #                 (4, 'Others'))
    LS_CHOICES = ((1, 'voluntary'),
                  (2, 'Dependent'),
                  # (3, 'Voluntary Delinquent'),
                  # (4, 'Dependent Delinquent'),
                  (5, 'Delinquent'))
    REF_CHOICES = (
        (1, 'Adams'), (2, 'Allegheny'), (3, 'Beaver'), (4, 'Bedford'),
        (5, 'Berks'), (6, 'Blair'), (7, 'Bucks'), (8, 'Butler'),
        (9, 'Cambria'), (10, 'Centre'), (11, 'Chester'), (12, 'Cumberland'),
        (13, 'Dauphin'), (14, 'Delaware'), (15, 'Erie'), (16, 'Fayette'),
        (17, 'Franklin'), (18, 'Huntingdon'), (19, 'Juniata'), (20, 'Kent'),
        (21, 'Lackawanna'), (22, 'Lancaster'), (23, 'Lebanon'),
        (24, 'Lehigh'), (25, 'Lycoming'), (26, 'Monroe'), (27, 'Montgomery'),
        (28, 'Montour'), (29, 'Northumberland'), (30, 'Perry'),
        (31, 'Philadelphia'), (32, 'Pike'), (34, 'Snyder'), (35, 'Tioga'),
        (36, 'Washington'), (37, 'Westmoreland'), (38, 'York'),
        (39, 'Armstrong'), (40, 'Columbia'), (41, 'Crawford'),
        (42, 'Cayahoga OH'), (43, 'Franklin OH'), (44, 'Greene'),
        (45, 'Indiana'), (46, 'Lawrence'), (47, 'MH'), (48, 'Mckean'),
        (49, 'Mercer'), (50, 'outside tri-county'), (51, 'Northampton'),
        (52, 'Pike'), (53, 'Schuylkill'), (54, 'Somerset'), (55, 'Union'),
        (56, 'Venango'), (57, 'Fulton'), (59, 'WV'), (60, 'SE PA'))
    CYF_CHOICES = ((0, 'None'), (1, 'CYF'), (2, 'Juvenile Justice'))
    no_or_yes = ((0, 'no'), (1, 'yes'))
    Termination_av = ((0, 'no'), (1, 'unknown'), (2, 'one'),
                      (3, 'two or more'))
    complaint = ((0, 'no'), (1, 'yes'), (9, 'N / A'))
    prior_awols_choice = ((0, 'none'), (1, 'one'), (2, 'two'), (3, 'many'))
    Borderline_IQ = ((0, '70+, or not listed assumed 70+'), (1, '<70'))
    foster_care_placements = ((0, 'no'), (1, 'one'), (2, 'two'),
                              (3, 'three or more'))
    prior_placements = ((0, 'no'), (1, 'one'), (2, 'two'),
                        (3, 'three or more'))
    Severe_MH_symptoms = ((0, 'no ER/hospitalizations'), (1, 'last 3 months'),
                          (2, '6 months ago'), (3, '9 months ago'),
                          (4, '1 year or more ago'))
    primary_lang_choices = ((1, 'English'), (2, 'not English'))
    second_lang = ((0, 'not at all'), (1, 'very little'), (2, 'average'),
                   (3, 'very well'))
    length_living_home = ((0, '0-6 months'), (1, '6-12 months'),
                          (2, '12+ months'))

    program_choices = ((1, 'substance abuse'), (2, 'sex offender'),
                       (3, 'intensive supervision'))

    facility_choices = ((1, 'Group Home'), (2, 'Secure'))
    level_choices = ((1, 'Mental Health'), (2, 'Intensive'))

    location_choices = (
        (1, 'Alliance'), (2, 'Anchor'), (3, 'Benet'), (4, 'Colony'),
        (5, 'Greystone'), (6, 'Hall'), (6, 'Hall/Loyalhannah'),
        (7, 'La Sa Quik'), (8, 'Marker'), (9, 'Middle Creek I'),
        (10, 'Middle Creek II'), (11, 'Middle Creek III'),
        (12, 'Monestery Run'), (13, 'Raphael'), (14, 'Susans'),
        (15, 'Sweeney'), (16, 'Vincent'), (17, 'Williams'), (18, 'manor')
    )

    program_model_suggested_choices = (
        (1, 'Substance Abuse Group Home'),
        (2, 'Sexual Offense Group Home with Mental Health Focus'),
        (3, 'Sexual offense facilities'),
        (4, 'Intensive Supervision Secure Facility for sexual offenses - '),
        (5, 'Intensive Supervision Group Home with Mental Health Focus'),
        (6, 'Intensive Supervision Group Homes'),
        (7, 'Intensive Supervision Secure Facilities')
    )

    referred_program_choices = (
        ("ISM", "ISM"), ("ISF", "ISF"), ("MHFO", "MHFO"), ("SUBAB", "SUBAB"),
        ("SEXOF-MH", "SEXOF-MH"), ("SEXOF-SECURE", "SEXOF-SECURE"),
        ("SEXOF", "SEXOF"), ("SECURE-MALE", "SECURE-MALE"),
        ("SECURE-FEMALE", "SECURE-FEMALE"),
        ("INDEPENDENT LIVING", "Independent Living"),
        ("Transitional Living", "Transitional Living")
    )

    episode_start = models.DateField(db_column='episode_start')
    episode_number = models.IntegerField(db_column='EpisodeNumber')
    client_code = models.IntegerField(db_column='Client_code',
                                      primary_key=True)
    name = models.CharField(db_column='name', max_length=100)
    last_name = models.CharField(db_column='Last_name', max_length=100)
    dob = models.DateField(db_column='dob')
    age = models.IntegerField(db_column='Age', null=True)
    gender = models.IntegerField(db_column='Gender', choices=GENDER_CHOICES)
    primary_language = models.IntegerField(db_column='primary_language',
                                           choices=primary_lang_choices)
    RefSourceCode = models.IntegerField(
        db_column='RefSourceCode')  # , choices=REF_CHOICES
    ls_type = models.IntegerField(db_column='LS_Type', choices=LS_CHOICES)
    CYF_code = models.IntegerField(db_column='CYF_code', choices=CYF_CHOICES)
    #  placement History
    number_of_prior_placements = models.IntegerField(
        db_column='Number_of_prior_placements',
        choices=prior_placements)
    number_of_foster_care_placements = models.IntegerField(
        db_column='Number_of_foster_care_placements',
        choices=foster_care_placements)
    number_of_prior_AWOLS = models.IntegerField(
        db_column='Number_of_prior_AWOLS',
        choices=prior_awols_choice)
    number_of_prior_treatment_terminations = models.IntegerField(
        db_column='Number_of_prior_treatment_terminations')
    termination_directly_to_AV = models.IntegerField(
        db_column='Termination_directly_to_AV',
        choices=Termination_av)
    length_of_time_since_living_at_home = models.IntegerField(
        db_column='Length_of_time_since_living_at_home',
        choices=length_living_home
    )
    hist_of_prior_program_SAO = models.IntegerField(
        db_column='Hist_of_prior_program_SAO',
        choices=no_or_yes)

    #  mental health
    autism_Diagnosis = models.IntegerField(db_column='Autism_Diagnosis',
                                           choices=no_or_yes)
    borderline_Personality = models.IntegerField(
        db_column='Borderline_Personality', choices=no_or_yes)
    reactive_Attachment_Disorder = models.IntegerField(
        db_column='Reactive_Attachment_Disorder',
        choices=no_or_yes)
    animal_cruelty = models.IntegerField(db_column='Animal_cruelty',
                                         choices=no_or_yes)
    schizophrenia = models.IntegerField(db_column='Schizophrenia',
                                        choices=no_or_yes)
    psychosis = models.IntegerField(db_column='Psychosis', choices=no_or_yes)
    borderline_IQ = models.IntegerField(db_column='Borderline_IQ',
                                        choices=Borderline_IQ)
    significant_mental_health_symptoms = models.IntegerField(
        db_column='Significant_mental_health_symptoms')
    prior_hospitalizations = models.IntegerField(
        db_column='prior_hospitalizations', blank=True)
    severe_mental_health_symptoms = models.IntegerField(
        db_column='Severe_mental_health_symptoms',
        choices=Severe_MH_symptoms)
    compliant_with_meds = models.IntegerField(db_column='Compliant_with_meds',
                                              choices=complaint)
    #####
    Exclusionary_Criteria = models.BooleanField(
        db_column='Exclusionary_Criteria',
        default=True)
    #####
    #  social/family Hx:
    incarcerated_caregivers = models.IntegerField(
        db_column='Incarcerated_caregivers',
        choices=no_or_yes,
        blank=True,
        null=True
    )
    death_Caregiver = models.IntegerField(db_column='Death_Caregiver',
                                          choices=no_or_yes, null=True)
    incarcerated_siblings = models.IntegerField(
        db_column='Incarcerated_siblings', choices=no_or_yes, null=True)
    death_Silblings = models.IntegerField(db_column='Death_Silblings',
                                          choices=no_or_yes, null=True)
    alcohol_Use = models.IntegerField(db_column='Alcohol_Use',
                                      choices=no_or_yes, null=True)
    drug_Use = models.IntegerField(db_column='Drug_Use',
                                   choices=no_or_yes, null=True)
    abuse_neglect = models.IntegerField(db_column='abuse_neglect',
                                        choices=no_or_yes, null=True)
    #  Assessment Score:
    yls_FamCircumstances_Score = models.IntegerField(
        db_column='YLS_FamCircumstances_Score', blank=True, null=True)
    yls_Edu_Employ_Score = models.IntegerField(
        db_column='YLS_Edu_Employ_Score', blank=True, null=True)
    yls_Peer_Score = models.IntegerField(db_column='YLS_Peer_Score',
                                         blank=True, null=True)
    yls_Subab_Score = models.IntegerField(db_column='YLS_Subab_Score',
                                          blank=True, null=True)
    yls_Leisure_Score = models.IntegerField(db_column='YLS_Leisure_Score',
                                            blank=True, null=True)
    yls_Personality_Score = models.IntegerField(
        db_column='YLS_Personality_Score', blank=True, null=True)
    yls_Attitude_Score = models.IntegerField(db_column='YLS_Attitude_Score',
                                             blank=True, null=True)
    yls_PriorCurrentOffenses_Score = models.IntegerField(
        db_column='YLS_PriorCurrentOffenses_Score',
        blank=True, null=True)
    family_support = models.IntegerField(db_column='family_support',
                                         null=True, blank=True)
    fire_setting = models.IntegerField(db_column='fire_setting',
                                       null=True, blank=True)
    level_of_aggression = models.IntegerField(db_column='level_of_aggression',
                                              null=True, blank=True)
    client_self_harm = models.IntegerField(db_column='Client_self_harm',
                                           blank=True, null=True)
    Screening_tool_Trauma = models.IntegerField(
        db_column='Screening_tool_Trauma',
        blank=True,
        null=True)

    cans_LifeFunctioning = models.IntegerField(
        db_column='CANS_LifeFunctioning', blank=True, null=True)
    cans_YouthStrengths = models.IntegerField(db_column='CANS_YouthStrengths',
                                              blank=True, null=True)
    cans_CareGiverStrengths = models.IntegerField(
        db_column='CANS_CareGiverStrengths', blank=True, null=True)
    cans_Culture = models.IntegerField(db_column='CANS_Culture', blank=True,
                                       null=True)
    cans_YouthBehavior = models.IntegerField(db_column='CANS_YouthBehavior',
                                             blank=True, null=True)
    cans_YouthRisk = models.IntegerField(db_column='CANS_YouthRisk',
                                         blank=True, null=True)
    cans_Trauma_Exp = models.IntegerField(db_column='CANS_Trauma_Exp',
                                          blank=True, null=True)

    # primaryRaceCode = models.IntegerField(db_column='PrimaryRacecode',
    #                                       choices=RACE_CHOICES, null=True)
    ageAtEpisodeStart = models.IntegerField(db_column='AgeAtEpisodeStart',
                                            null=True)
    ageAtEnrollStart = models.IntegerField(db_column='AgeAtEnrollStart',
                                           null=True)

    # sexually_acting_out_in_past_program = models.IntegerField(
    #     db_column='sexually_acting_out_in_past_program',
    #     choices=SAO_past_program)

    #############################
    modified_date = models.DateTimeField(
        db_column='Modified_Date',
        auto_now=True)

    program = models.IntegerField(db_column='Program')
    model_program = models.CharField(db_column='Model_Program',
                                     max_length=100)
    confidence = models.IntegerField(db_column='Confidence')
    facility_type = models.IntegerField(db_column='facility_pred')

    client_selected_program = models.CharField(max_length=100)

    client_selected_level = models.CharField(max_length=100)
    client_selected_facility = models.CharField(max_length=100)
    client_selected_locations = models.CharField(max_length=100)

    Program_Completion = models.IntegerField(db_column='Program_Completion',
                                             choices=no_or_yes, null=True)
    Returned_to_Care = models.IntegerField(db_column='Returned_to_Care',
                                           choices=no_or_yes, null=True)
    program_significantly_modified = models.IntegerField(
        db_column='program_significantly_modified',
        choices=no_or_yes,
        null=True)

    level_of_care = models.IntegerField(db_column='level_of_care')

#####################################

    enrollStart_date = models.DateField(db_column='enrollStart_date',
                                        blank=True, null=True)
    english_second_lang = models.IntegerField(db_column='english_second_lang',
                                              choices=second_lang, null=True)
    type_of_drugs = models.TextField(db_column='type_of_drugs', blank=True,
                                     null=True)
    FAST_FamilyTogetherScore = models.IntegerField(
        db_column='FAST_FamilyTogetherScore', blank=True, null=True)
    FAST_CaregiverAdvocacyScore = models.IntegerField(
        db_column='FAST_CaregiverAdvocacyScore', blank=True, null=True)

    referred_program = models.CharField(
        db_column='referred_program',
        max_length=100,
        choices=referred_program_choices
    )  # ,choices = referred_program_choices,null = True
    inclusionary_criteria = models.BooleanField(
        db_column='inclusionary_criteria',
        default=True
    )
    condition_program = models.IntegerField(db_column='condition_program')

    roc_confidence = models.IntegerField(db_column='roc_confidence',blank=True, null=True)
    # client_selected_program = models.CharField(max_length=10,
    #                                            choices=program_choices)
    #
    # client_selected_level = models.CharField(max_length=10,
    #                                          choices=level_choices)
    # client_selected_facility = models.CharField(max_length=10,
    #                                             choices=facility_choices)
    # client_selected_locations = models.CharField(max_length=100,
    #                                              choices=location_choices)
    #
    # program_model_suggested = models.CharField(max_length=100,
    #                                            choices=program_model_suggested_choices)


# ##  Char


class ListFormField(forms.CharField):
    def to_python(self, value):
        if value is None:
            value = ""
        return value.split(",")

    def prepare_value(self, value):
        if value is None:
            value = []
        return ",".join(value)


class CustomListField(models.ListField):
    def formfield(self, **kwargs):
        return ListFormField(max_length=1000)

# #  INt


class ListFormIntField(forms.CharField):
    def to_python(self, value):
        if value is None:
            value = ""
        # return value.split(",")
        return list(map(int, value.split(",")))

    def prepare_value(self, value):
        if value is None:
            value = []
        return ",".join(map(str, value))


class CustomListIntField(models.ListField):
    def formfield(self, **kwargs):
        return ListFormIntField()


class Adelphoi_Mapping(models.Model):
    _id = models.ObjectIdField()
    #  id = models.AutoField()
    program = models.IntegerField(db_column='program')
    program_name = models.CharField(db_column='program_name', max_length=100)

    gender = models.IntegerField(db_column='gender')
    gender_name = models.CharField(db_column='gender_name', max_length=20)

    level_of_care = models.IntegerField(db_column='level_of_care')
    level_names = models.CharField(db_column='level_names', max_length=100)
    location = CustomListIntField()
    location_names = CustomListField()
    facility_type = models.IntegerField(db_column='facility_type')
    facility_names = models.CharField(db_column='facility_names',
                                      max_length=100)

    program_model_suggested = models.CharField(
        db_column='program_model_suggested', max_length=100)

    program_type = models.CharField(db_column='program_type', max_length=100)
    default_level_facility = models.BooleanField(
        db_column='default_level_facility',default=True)


class ProgramModel(models.Model):
    program = models.IntegerField(db_column='program', unique=True)
    program_name = models.CharField(db_column='program_name', max_length=100)


class ModelLocation(models.Model):
    location = models.IntegerField(db_column='location', unique=True)
    location_names = models.CharField(
        db_column='location_names', max_length=100)


class LevelModel(models.Model):
    level_of_care = models.IntegerField(db_column='level_of_care',
                                        unique=True)
    level_names = models.CharField(db_column='level_names', max_length=100)


class FacilityModel(models.Model):
    facility_type = models.IntegerField(db_column='facility_type',
                                        unique=True)
    facility_names = models.CharField(db_column='facility_names',
                                      max_length=100)


class ReferralSource(models.Model):
    referral_code = models.IntegerField(db_column='referral_code',
                                        unique=True)
    referral_name = models.CharField(db_column='referral_name',
                                     max_length=100)
