# Generated by Django 2.2.7 on 2020-02-05 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstMatch', '0002_auto_20200131_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='modeltests',
            name='inclusionary_criteria',
            field=models.BooleanField(db_column='inclusionary_criteria', default=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='FAST_CaregiverAdvocacyScore',
            field=models.IntegerField(blank=True, db_column='FAST_CaregiverAdvocacyScore', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='FAST_FamilyTogetherScore',
            field=models.IntegerField(blank=True, db_column='FAST_FamilyTogetherScore', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='Screening_tool_Trauma',
            field=models.IntegerField(blank=True, db_column='Screening_tool_Trauma', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='abuse_neglect',
            field=models.IntegerField(choices=[(0, 'no'), (1, 'yes')], db_column='abuse_neglect', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='cans_CareGiverStrengths',
            field=models.IntegerField(blank=True, db_column='CANS_CareGiverStrengths', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='cans_Culture',
            field=models.IntegerField(blank=True, db_column='CANS_Culture', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='cans_LifeFunctioning',
            field=models.IntegerField(blank=True, db_column='CANS_LifeFunctioning', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='cans_Trauma_Exp',
            field=models.IntegerField(blank=True, db_column='CANS_Trauma_Exp', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='cans_YouthBehavior',
            field=models.IntegerField(blank=True, db_column='CANS_YouthBehavior', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='cans_YouthRisk',
            field=models.IntegerField(blank=True, db_column='CANS_YouthRisk', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='cans_YouthStrengths',
            field=models.IntegerField(blank=True, db_column='CANS_YouthStrengths', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='client_self_harm',
            field=models.IntegerField(blank=True, db_column='Client_self_harm', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='family_support',
            field=models.IntegerField(blank=True, db_column='family_support', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='fire_setting',
            field=models.IntegerField(blank=True, db_column='fire_setting', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='length_of_time_since_living_at_home',
            field=models.IntegerField(choices=[(0, '0-6 months'), (1, '6-12 months'), (2, '12+ months')], db_column='Length_of_time_since_living_at_home'),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='level_of_aggression',
            field=models.IntegerField(blank=True, db_column='level_of_aggression', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_Attitude_Score',
            field=models.IntegerField(blank=True, db_column='YLS_Attitude_Score', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_Edu_Employ_Score',
            field=models.IntegerField(blank=True, db_column='YLS_Edu_Employ_Score', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_FamCircumstances_Score',
            field=models.IntegerField(blank=True, db_column='YLS_FamCircumstances_Score', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_Leisure_Score',
            field=models.IntegerField(blank=True, db_column='YLS_Leisure_Score', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_Peer_Score',
            field=models.IntegerField(blank=True, db_column='YLS_Peer_Score', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_Personality_Score',
            field=models.IntegerField(blank=True, db_column='YLS_Personality_Score', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_PriorCurrentOffenses_Score',
            field=models.IntegerField(blank=True, db_column='YLS_PriorCurrentOffenses_Score', null=True),
        ),
        migrations.AlterField(
            model_name='modeltests',
            name='yls_Subab_Score',
            field=models.IntegerField(blank=True, db_column='YLS_Subab_Score', null=True),
        ),
    ]
