from rest_framework import serializers
# from rest_framework import ModelTests
from .models import (ModelTests, Adelphoi_Mapping,
                     ProgramModel, ModelLocation,
                     ReferralSource)


class ModelTestsSerializers(serializers.ModelSerializer):

    class Meta:
        model = ModelTests
        # fields ='__all__'
        exclude = [
            'modified_date', 'program', 'model_program',
            'confidence', 'level_of_care', 'facility_type',
            'client_selected_program', 'client_selected_level',
            'client_selected_facility', 'client_selected_locations',
            'Program_Completion', 'Returned_to_Care',
            'condition_program', 'referred_program', 'roc_confidence'
            ]  # ,,'client_selected_program','client_selected_level',
        # 'client_selected_facility'


class Adelphoi_placementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = ['referred_program', 'model_program']


class ModelTestsSerializers_selected_program(serializers.ModelSerializer):

    # ModelTestsSerializers(required=True)

    class Meta:
        model = ModelTests
        fields = ['client_selected_program',
                  'client_selected_level',
                  'client_selected_facility',
                  'client_selected_locations'
                  ]  # ,'client_selected_level','client_selected_facility'


class ModelTestsSerializer_program_model_suggested(serializers.
                                                   ModelSerializer):

    class Meta:
        model = ModelTests
        fields = ['client_selected_program',
                  'client_selected_level',
                  'client_selected_facility',
                  'client_selected_locations']


class ProgramSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = ['client_selected_program']


class LocationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = ['client_selected_locations']


class ProgramLocationSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = ['client_selected_program', 'client_selected_locations']


class ProgramLevelSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = ['Program_Completion',
                  'Returned_to_Care',
                  'program_significantly_modified']


class FilterSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = '__all__'


class AdminInterface(serializers.ModelSerializer):
    class Meta:
        model = Adelphoi_Mapping
        fields = '__all__'
        # fields = ['gender','program']


# class LocationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ModelTests
#         fields = ['client_selected_locations']


class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['model_program', 'referred_program']


class Adelphoi_referredSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = ['referred_program']


class ProgramIndSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModel
        fields = ['program', 'program_name']


class ReferralIndSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralSource
        fields = ['referral_code', 'referral_name']


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModel
        fields = ['program_name']


class refferalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralSource
        fields = ['referral_name']


class LocationIndSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelLocation
        fields = ['location', 'location_names']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelLocation
        fields = ['location_names']


class Available_programSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramModel
        fields = ['program', 'program_name']


class Program_PCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        fields = ['client_selected_program']


class UpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = ModelTests
        exclude = [
            'client_code', 'modified_date', 'program', 'model_program',
            'confidence', 'level_of_care', 'facility_type',
            'client_selected_program', 'client_selected_level',
            'client_selected_facility', 'client_selected_locations',
            'Program_Completion', 'Returned_to_Care', 'condition_program','referred_program'
        ]
