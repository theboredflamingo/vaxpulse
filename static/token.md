access token: pk.eyJ1Ijoic3MwMzAzIiwiYSI6ImNscmt3anN3NzBnaHoycXFlODQybmlubnUifQ.LbaUB1B1ncsiSP6ZPGqbJQ
"""def calculate_vaccination_date(date_of_birth):
    # Define your vaccination schedule based on age
    vaccine_schedule = {
        1:'Hepatitis-B Hepatitis-A MMR Varicella DTaP Influenza HPV IPV',
        2: 'Hepatitis-B Influenza',
        3:'Influenza',
        4: 'DTP Polio Hepatitis-B Rotavirus Varicella MMR',
        5:'DTP Polio Hepatitis-B Rotavirus Varicella MMR',
        6: 'DTP Polio Hepatitis-B Rotavirus Varicella MMR',
        7:'HPV Influenza',
        8:'HPV Influenza',
        9:'HPV Influenza',
        10:'HPV Influenza',
        11:'Influenza HPV MenACWY Tdap',
        12:'Influenza HPV MenACWY Tdap',
        13:'Influenza MenACWY MenB MenABCWY',
        14:'Influenza MenACWY MenB MenABCWY',
        15:'Influenza MenACWY MenB MenABCWY',
        16:'Influenza MenACWY MenB MenABCWY',
        17:'Influenza MenACWY MenB MenABCWY',
        18:'Influenza MenACWY MenB MenABCWY',
        # Add more entries as needed
    }

    # Calculate age
    birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d')
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    # Calculate recommended vaccine based on age
    recommended_vaccine = vaccine_schedule.get(age, 'No recommended vaccine')

    # Calculate updating date for the vaccine
    updating_date = birth_date + timedelta(days=365 * age)
    while(age < 18):
        return age, recommended_vaccine, updating_date.strftime('%Y-%m-%d')
        age = age + 1
        recommended_vaccine = vaccine_schedule.get(age, 'No recommended vaccine')
        updating_date = birth_date + timedelta(days=365 * age)
    return age, recommended_vaccine, updating_date.strftime('%Y-%m-%d')"""

