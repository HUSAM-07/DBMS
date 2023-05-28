# Core Pkgs
import streamlit as st 
import pandas as pd

# DB Mgmt
import sqlite3 
conn = sqlite3.connect('world.sqlite')
c = conn.cursor()


# Fxn Make Execution
def sql_executor(raw_code):
    if 'CALL' in raw_code:
        procedure_name = raw_code.split()[1]
        parameters = raw_code.split('(')[1].split(')')[0].split(',')
        parameter_values = []
        for parameter in parameters:
            parameter_value = parameter.strip().strip("'")
            parameter_values.append(parameter_value)
        placeholders = ', '.join(['?' for _ in range(len(parameter_values))])
        query = f"CALL {procedure_name}({placeholders})"
        c.execute(query, parameter_values)
        data = c.fetchall()
    else:
        c.execute(raw_code)
        data = c.fetchall()
    return data



city = ['ID,', 'Name,', 'CountryCode,', 'District,', 'Population']
country = ['Code,', 'Name,', 'Continent,', 'Region,', 'SurfaceArea,', 'IndepYear,', 'Population,', 'LifeExpectancy,', 'GNP,', 'GNPOld,', 'LocalName,', 'GovernmentForm,', 'HeadOfState,', 'Capital,', 'Code2']
countrylanguage = ['CountryCode,', 'Language,', 'IsOfficial,', 'Percentage']




def main():
	st.title("Country Directory")
	st.subheader("Name: Mohammed Husamuddin | 2021A7PS0150U")

	menu = ["Home","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("HomePage")

		# Columns/Layout
		col1,col2 = st.columns(2)

		with col1:
			with st.form(key='query_form'):
				raw_code = st.text_area("SQL Code Here")
				submit_code = st.form_submit_button("Execute")

			# Table of Info

			with st.expander("Table Info"):
				table_info = {'city':city,'country':country,'countrylanguage':countrylanguage}
				st.json(table_info)
			
		# Results Layouts
		with col2:
			if submit_code:
				st.info("Query Submitted")
				st.code(raw_code)

				# Results 
				query_results = sql_executor(raw_code)
				with st.expander("Results"):
					st.write(query_results)

				with st.expander("Pretty Table"):
					query_df = pd.DataFrame(query_results)
					st.dataframe(query_df)


	else:
		st.subheader("About")





if __name__ == '__main__':
	main()
