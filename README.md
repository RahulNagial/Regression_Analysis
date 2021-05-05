# Regression_Analysis
## Calgary Monthly Rent Predictor: Project Overview 
* Created a tool that estimates monthly rent (MAE ~ $ 160) for Calgary, Canada to help people negotiate rent.
* Scraped ~1500 entries from RentFaster (one of the most popular rental listing websites in Canada) using python and selenium.
* Engineered features (such as number of beds/baths, neighbourhood, square footage, monthly rent) from raw data.
* Performed exploratory data analysis to remove outliers and shortlist variables for machine learning model building.
* Optimized Ridge, Random Forest and XGBoost regression using GridsearchCV.
* Built a client facing API using Flask and deployed it on a local webserver. 

This project will potentially benefit:
* Immigrants - newcomers to the city would be interested in knowing how much is the monthly rent so they can plan accordingly.
* International Students - students need a benchmark against which they can negotiate the rent landlords are quoting.  
* Renters (in general) - any potential renter is interested in knowing how much a specific type of rental place would cost.
* Landlords - they can get a better sense of what other landlords are charging in city and thus, they can quote rent at a more competitive value.

The code workflow is in the following order:
* rentfasterscraping.py 
* Data_Cleaning_and_Introductory_EDA.ipynb 
* Exploratory_Data_Analysis_and_Data_Cleaning .ipynb
* Model_Building_Tuning_Evaluation.ipynb
* app.py

## Code and Resources Used 
**Python Version:** 3.8  
**Packages:** pandas, numpy, sklearn, matplotlib, seaborn, selenium, flask, pickle, itertools, nltk <br>
**For Web Framework Requirements:**  ```pip install -r requirements.txt```  <br>
**GitHub Repo Ref_1:** https://github.com/PlayingNumbers/ds_salary_proj <br>
**GitHub Repo Ref_2:** https://github.com/krishnaik06/Heroku-Demo

## Web Scraping
Wrote a script in python (using selenium) to scrape ~1500 rental listings from rentfaster.ca. Each listing had information regarding the following:
* Monthly Rent
*	Pet Allowance
*	Heat, Water, Other Utilities
*	Listing Description
*	Neighbourhood
*	Listing Type
*	Car Parking Provision
*	Sq. Feet Area 

And other features like the aforementioned.

## Data Cleaning
After scraping the data, I needed to clean it up so that it was usable for our model. I made the following changes (among others):

*	Parsed monthly rent out of text 
*	Made column for listing type  
*	Removed rows with outliers 
*	Parsed information regarding pet allowance out of text 
*	Made a new column for parking status  
*	Added a column for length of listing ad title/description  
*	Transformed construction date into age of listing 
*	Added column for neighbourhood 

I also engineered data and added scoring for features such as:
* Utilities
* Building
* Property
* Community


## Exploratory Data Analysis (EDA)
I looked at the distributions of the numerical data and the value counts for the various categorical variables. I also studied the correlation between different variables and the monthly rent. Below are a few highlights from the exploratory data analysis. 

<img src="https://user-images.githubusercontent.com/80373488/117212103-210c3280-adb7-11eb-8bdf-baa1aa11a0e5.png" width="450" height="450"><img src="https://user-images.githubusercontent.com/80373488/117212118-27021380-adb7-11eb-9470-c6a710303177.png" width="450" height="450">
<img src="https://user-images.githubusercontent.com/80373488/117212132-2f5a4e80-adb7-11eb-8149-84ece661043b.png" width="450" height="450">
<img src="https://user-images.githubusercontent.com/80373488/117212138-31bca880-adb7-11eb-99c2-7e725de72b23.png" width="450" height="450">
<img src="https://user-images.githubusercontent.com/80373488/117212160-384b2000-adb7-11eb-964b-28321c4f590b.png" width="450" height="450">
<img src="https://user-images.githubusercontent.com/80373488/117212184-40a35b00-adb7-11eb-96bb-5f4dee8ee9dc.png" width="225" height="450">

## Model Building 
First, I transformed the categorical variables (listing type and neighbourhood) into dummy variables. I also split the data into train and tests sets with a test size of 20%.   

I tried three different models and evaluated them using Mean Absolute Error (MAE). I chose MAE because it is relatively easy to interpret and outliers aren’t particularly bad in for this type of model.   

I tried three different models:
*	**Ridge Regression** – Baseline for the models. I thought a regularized regression like ridge would be effective in avoiding overfitting.
*	**Random Forest Regression** – Because of the sparse data from the many categorical variables, I thought a ensemble-decision tree based model would be effective.
*	**XGBoost Regression** – Again, with the sparsity associated with the data, I thought that this would be a good fit. XGBoost is very fast due to gradient boosting and thus, is routinely used in industry for gettting optimized results. 

## Model Performance
The XGBoost model far outperformed the other approaches on the training and test sets. 
*	**Ridge Regression** : MAE = $210
*	**Random Forest Regression**: MAE = $172
*	**XGBoost Regression**: MAE = $160

## Productionization 
In this step, I built a Flask API endpoint that was hosted on a local webserver. The API endpoint rendered a HTML GUI which takes in a request with a list of features regarding the listing and returns an estimated monthly rent for such a listing. 

In the image below the rendered HTML GUI hosted on local webserver is shown.

<img src="https://user-images.githubusercontent.com/80373488/117215117-0471f980-adbb-11eb-8b1d-ac96d0b55c7c.png" width="1000" height="200">

On putting in the paramters and clicking on *predict*, the GUI returns the expected monthly rent for such a listing in Calgary (refer image below).

<img src="https://user-images.githubusercontent.com/80373488/117215135-0d62cb00-adbb-11eb-8e6d-5b0620397caf.png" width="1000" height="250">

## Future Improvements
There is scope for improvement in this project in the following areas:
* The model was deployed only on local webserver. In order to make it accessible to anyone online, it should be deployed on cloud servers like Heroku or AWS EC2 instance.
* Natural Language Processing (NLP) can be used to gain insights in the rental listing text.
* Transformations can be applied on left/right skewed variables to convert them to Gaussian distribution and see if this improves model accuracy.
