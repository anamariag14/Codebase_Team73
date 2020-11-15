# Codebase_Team73
SmartFlow is a project that intend to estimate the number freight vehicles in specific corridors of Bogota (Calle 80 and Calle 13), at a especific hour, weekday and month of the year. To accomplish this, two databases (Bitcarrier and RNDC) were used to implement a XGBoost model. 

In this repository you will find a notebook for each database, one notebook to merge both databases, and for the model exist one file for each corridor and direction (four in total).

1. Bitcarier database analysis exploration: 'Bitcarrier_DB_Exploration.ipynb'
2. RNDC database analysis exploration: 'RNDC_DB_Exploration.ipynb'
3. Merging both databases: 'Unique_view.ipynb'
4. Models for the estimation of freight vehicles
   1. Model for Calle 13 East-West direction: 'Model_Cl13_EW.ipynb'
   2. Model for Calle 13 West-East direction: 'Model_Cl13_WE.ipynb'
   3. Model for Calle 80 East-West direction: 'Model_Cl80_EW.ipynb'
   4. Model for Calle 80 West-East direction: 'Model_Cl80_WE.ipynb'

        
