import pandas as pd
import numpy as np
from pystan import StanModel
from patsy import dmatrix
import pickle

# Load the data file
mice_new = pd.read_csv("/media/data_cifs/projects/prj_fallon/8_Month_Data/ACBM_5XFAD_8month.csv",
                       dtype={'Day of Recording': 'float64', 'Hour (0-23)': 'float64', 'drink': 'float64',
                              'eat': 'float64', 'groom': 'float64', 'hang': 'float64', 'sniff': 'float64',
                              'rear': 'float64', 'rest': 'float64', 'walk': 'float64', 'eathand': 'float64'})

# Fix names of the columns
mice_5XFAD = mice_new.rename(columns={"Mouse ID": "MouseID", "Genotype": "Genotype", "Gender": "Gender",
                                      "Age": "Age", "Day of Recording": "Day", "Hour (0-23)": "Hour",
                                      "Date": "Date", "drink": "Drink", "eat": "Eat",
                                      "groom": "Groom", "hang": "Hang", "sniff": "Sniff",
                                      "rear": "Rear", "rest": "Rest", "walk": "Walk",
                                      "eathand": "EBH"})

# Reorder columns
mice_5XFAD = mice_5XFAD[["MouseID", "Genotype", "Gender", "Age", "Day", "Hour",
                         "Date","Drink", "Eat", "EBH", "Groom",
                         "Hang", "Rear", "Rest", "Sniff", "Walk"]]

# Create a factor for GenotypeFAD
mice_5XFAD['GenotypeFAD'] = np.where(mice_5XFAD['Genotype'] == 'Hemi', 1, 0)

# Filter data for p180 age
mice_5XFAD_p180 = mice_5XFAD

# Assign unique IDs to mice
mice_5XFAD_p180['id'] = mice_5XFAD_p180['MouseID'].apply(lambda x: list(mice_5XFAD_p180['MouseID'].unique()).index(x) + 1)

# Define smart_round function
def smart_round(x):
    y = np.floor(x)
    indices = np.argsort(x - y, axis=1)[:, -np.round(x.sum(axis=1) - y.sum(axis=1)).astype(int)]
    for i in range(len(indices)):
        y[i, indices[i]] += 1
    return y

outcomes_int = smart_round(mice_5XFAD_p180.iloc[:, 8:16].values)

Y = outcomes_int

# Create design matrix X
X = dmatrix('0 + C(GenotypeFAD)', data=mice_5XFAD_p180, return_type='dataframe').values

mice_id = mice_5XFAD_p180['id'].values

nd = len(np.unique(mice_id))

days = mice_5XFAD_p180['Day'].values

ndays = len(np.unique(days))

hour_dat = mice_5XFAD_p180['Hour'].values

num_data = len(hour_dat)

# Define B-spline basis matrix for Hour
from patsy import bs
Bsplines = bs(hour_dat, df=4, include_intercept=True)
num_basis = Bsplines.shape[1]

data4Stan = {
    'N': Y.shape[0],
    'ncolY': Y.shape[1],
    'ncolX': X.shape[1],
    'X': X,
    'Y': Y,
    'num_data': num_data,
    'num_basis': num_basis,
    'Bsplines': Bsplines,
    'nd': nd,
    'mice_id': mice_id,
    'days': days,
    'ndays': ndays
}

# Compile and run Stan model
with open('/media/data_cifs/projects/prj_fallon/5XFAD_Analysis', 'r') as file:
    stan_model_code = file.read()


stan_model = StanModel(model_code=stan_model_code)
fitCalc = stan_model.sampling(data=data4Stan, chains=1, warmup=2, iter=10, cores=1, control={'max_treedepth': 15, 'adapt_delta': 0.95})

# Save the fitted model object
with open("ZIGDM_Sep24_RSIGQ_Simple_5XFAD_8mo_taus.pkl", 'wb') as f:
    pickle.dump(fitCalc, f)

# Obtain posterior draws and save them
posterior_draws = fitCalc.extract(permuted=True)
posterior_df = pd.DataFrame(posterior_draws)
index = np.arange(0, 10000, 4)
posterior_df_sml = posterior_df.iloc[index]

posterior_df_sml.to_pickle("ZIGDM_Sep24_RSIGQ_Simple_posterior_5XFAD_8mo_taus_sml.pkl")