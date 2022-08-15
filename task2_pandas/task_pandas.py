import py7zr
from glob import glob
import os
import pandas as pd

# setting path_ variable to data/
path_data = '.' + os.sep + 'data' + os.sep

# opening file containing the password
file_ = path_data + 'pass.txt'
with open(file_, encoding='utf-8') as f:
   password = f.readline()

# opening password protected 7z file using py7zr library
file_ = path_data + 'books_data.7z'
with py7zr.SevenZipFile(file_, mode='r', password=password) as z:
    z.extractall(path=path_data)

# searching for all *.csv files should be only one
csv_files = glob(f'{path_data}*.csv')
if len(csv_files) > 1:
    print('There should be only one CSV file')

book_file = csv_files[0]
book_file = book_file.split(os.sep)[-1]

file_ = path_data + book_file

# Initial regex pattern
# df = pd.read_csv(f, sep=',(?=\s{2})|,(?=\w)|,(?=")|,(?=\')|,(?=¡)|,(?=\$)|,(?=¿)', engine='python')
# shortened regex pattern
# df = pd.read_csv(f, sep=',(?=\s{2})|,(?=[\w\"\'¡\$¿])', engine='python')

# streamlined regex pattern
# importing csv using pandas, keeping isbn13 column as string (so that 0's aren't truncated)
df = pd.read_csv(file_, sep=',(?=\s{2})|,(?=[^ ])', dtype={'ISBń13': object}, engine='python')

# extracting columns from df and processing them using map
new_columns = df.columns
new_columns = map(str.lower, new_columns)
new_columns = map(str.strip, new_columns)

# creating tupes with pl and unocode letters to create a dictionary
pl = tuple('ąćęłńóśżź')
un = tuple('acelnoszz')
pl_to_latin = dict(zip(pl, un))

#  creating translation table for str.translate
pl_lat_table = str.maketrans(pl_to_latin)

# using lambda function to do str.translate, converting map object back to list
# and appending it as new column names of the dataframe
new_columns = map(lambda s: s.translate(pl_lat_table), new_columns)
new_columns = list(new_columns)
df.columns = new_columns

# setting bookid as new index, inplace
df.set_index('bookid', inplace=True)

# setting directory/filename for .parquet export
path_transformed = path_data + 'transformed' + os.sep
file_ = path_transformed + book_file
file_ = file_[:-4] + '.parquet'

# if data/transformed directory doesn't exist create it
path_ = path_data + '*' + os.sep
list_dirs = glob(path_)

# checking whether transformed directory exists
if path_transformed not in list_dirs:
    os.mkdir(path_transformed)

# exporting to parquet format, requires pyarrow or fastparquet
df.to_parquet(file_)

# Task 5a) "Top 50 books"

# sorting and picking the top n values can sometimes be faster than nlargest, but documentation recommends nlargest
df_top_50 = df.nlargest(400, 'ratings_count')
df_top_50 = df_top_50.nlargest(50, 'average_rating')

# same as above using sorting and slicing
# df_top_50 = df.sort_values('ratings_count', ascending=False)
# df_top_50 = df_top_50[:400]
# df_top_50 = df_top_50.sort_values('average_rating', ascending=False)
# df_top_50 = df_top_50[:50]

# file directory and Excel sheet name setting
path_ = '.' + os.sep + 'data' + os.sep + 'transformed' + os.sep
f = path_ + book_file[:-4] + '.xlsx'
task_name = "Top 50 books"

# exporting as new file with a specific sheet name - not adding a new sheet to a file
df_top_50.to_excel(f, sheet_name=task_name)


# Task 5b) "Best books before 2000s"

# function to be used by df.apply method to return True if book was published before 2000
def bef_2000(r):
    if int(r[-4:]) < 2000:
        return True
    else:
        return False


# using a function to do a one-line mask
df_best_bef_2000 = df[df['publication_date'].apply(bef_2000)]
df_best_bef_2000 = df_best_bef_2000.sort_values('average_rating', ascending=False)

# deleting isbn13 column, inplace
del df_best_bef_2000['isbn13']

# setting task name
task_name ='Best books before 2000s'

# appending the df as new sheet to an existing Excel sheet
with pd.ExcelWriter(f, mode='a') as writer:
    df_best_bef_2000.to_excel(writer, sheet_name=task_name)


# Task 5c) "University Published"

# function to be used by df.apply method to return True if the book was 'academic'
def academic(r):
    if 'academic' in r.lower() or 'university' in r.lower():
        return True
    else:
        return False

# using a function to do a one-line mask
df_university = df[df['publisher'].apply(academic)]

# sorting the df by average_rating
df_university = df_university.sort_values('average_rating', ascending=False)

# deleting isbn13 column, inplace
del df_university['isbn13']

# setting task name
task_name = 'University Published'

# appending the df as new sheet to an existing Excel sheet
with pd.ExcelWriter(f, mode='a') as writer:
    df_university.to_excel(writer, sheet_name=task_name)


# Task 5d) "Best short stories"
# applying a one line two condition mask where number of pages is below 100 and amount of ratings is above 1000
df_short_stories = df[ (df['num_pages'] < 100) & (df['ratings_count'] > 1000) ]

# getting the largest 50 items by average_rating column
df_short_stories = df_short_stories.nlargest(50, 'average_rating')

# same doing it through sorting way
# df_short_stories = df_short_stories.sort_values('average_rating', ascending=False)
# df_short_stories = df_short_stories[:50]

# setting task name
task_name = "Best short stories"

# appending the df as new sheet to an existing Excel sheet
with pd.ExcelWriter(f, mode='a') as writer:
    df_short_stories.to_excel(writer, sheet_name=task_name)

# 5e) "Most popular author"
# chaining: group by authors, sum by amount of ratings
df_popular_author = df.groupby(by=['authors'])['ratings_count'].sum()

# sort the series by remaining column (ratings_count) and get the top value - which is the author
pop_author = df_popular_author.sort_values(ascending=False).index[0]

# use the top author to make a one line mask
df_popular_author = df[df['authors'] == pop_author]

# sort the remaining df by average rating
df_popular_author = df_popular_author.sort_values('average_rating', ascending=False)

# setting task name
task_name = "Most popular author"

# appending the df as new sheet to an existing Excel sheet
with pd.ExcelWriter(f, mode='a') as writer:
    df_popular_author.to_excel(writer, sheet_name=task_name)