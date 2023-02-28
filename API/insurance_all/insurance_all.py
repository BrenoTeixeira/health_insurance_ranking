class InsuranceAll(object):

    def transformation(self, test):

        new_cols = [col.lower() for col in test.columns.to_list()]

        test.columns = new_cols
        
        test['id' ] = test['id'].astype('int64')
        test['gender'] = test['gender'].astype('object')
        test['age'] = test['age'].astype('int64')
        test['region_code'] = test['region_code'].astype('float64')
        test['policy_sales_channel'] = test['policy_sales_channel'].astype('float64')
        test['previously_insured'] = test['previously_insured'].astype('int64')
        test['annual_premium'] = test['annual_premium'].astype('float64')
        test['vintage'] = test['vintage'].astype('int64')
        test['driving_license'] = test['driving_license'].astype('int64')
        test['vehicle_age'] = test['vehicle_age'].astype('object')
        test['vehicle_damage'] = test['vehicle_damage'].astype('object')

        return test

    def feature_engineering(self, test):

        test['vehicle_age'] = test['vehicle_age'].apply(lambda x: 'over_2_years' if x == '> 2 Years' else 'between_1_2_year' if x== '1-2 Year' else 'under_1_year')

        test['vehicle_damage'] = test['vehicle_damage'].apply(lambda x: 1 if x == 'Yes' else 0)

        return test
    

