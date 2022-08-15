## Solution to the Lambda word count/fibonacci task

### Uploading files
To upload (or put in AWS nomenclature) I use the AWS boto3 library.

I don't upload actual files, rather bytes objects encoded in UTF-8 converted from strings created on my own (fibonacci digits) or json.dumps() method (word count).

I pass the bytes object to the boto3.client('s3').put_object() method, which uploads it as a file on the bucket.

The file names are in the format: %Y_%m_%d__%H_%M_%S__%f
Example names for two subtasks are:
2022_08_15__14_38_44__130387.json
2022_08_15__14_38_44__130387.csv

The file names are generated from time/date using filename_now() function.

### lambda_handler function
I initialize the s3 variable as a client using boto3 library.

I read the post data from the event object to the body variable.
I convert(str.join) body to a long string.

I use regular expressions to find all the integers and all words in the body. The result I pass into the following functions dedicated to specific tasks.

#### fibonacci integers
I pass the numbers to the fibonacci_process function which as a result returns as string object that holds header and coma separated values.


##### fibonacci_process() function
Firsts the numbers list is converted to set and then back to list to eliminate non unique numbers (as is in the example output). Then numbers are converted from string to int using list comprehension.

Then the numbers are sorted (as in the example output the numbers are sorted). 

Once cache is generated the sequence and cache are passed to the numbers_to_csv_string function that goes from left to right and does a few things, each time adding a row of CSV data to the output string.

First it checks whether numbers from the left are smaller then 0, and since they are sorted and negative numbers can't be in the fibonacci sequence we can add the numbers to the output (CSV string), move pointer(increment by 1; pointer - a variable used to index the list) to the right so we can just iterate over the rest of the numbers (leftover positive numbers).

Then we check if the first leftover number from the left is equal to 0 and adding proper output to the output. Because that's the first fibonacci number in the sequence and has no number on the left it's best to deal with it as it should be treated exceptionally. We do similar process for 1.

Then we continue going from the left and try to match it to a number in the fibonacci sequence from smallest (going through the sequence till current number equals or is bigger then the number from input). If the number ends up to be a member of the sequence then previous, this and next variables with comas between them are added to the string. If not, just the number with two comas around is added to the result output instead.

We end up with a generated CSV string by adding numbers with comas and line breaks.
Back in the lambda_handler function we pass the result into the bytes function and upload to the bucket.

The key is that we don't use recursion to generate fibonacci sequence by adding two previous ones recursively. That at worst case has a cost of O(2<sup>n</sup>).

Initially I solved it using dynamic programming and generating a cache (sequence of fibonacci numbers up to the largest number from the input + next number in fib sequence). That solution is much faster but we have to store the cache in memory. I quickly realized that we can just use 3 variables and go through the sequence of input numbers and check whether they match a fibonacci number generated on the fly.

Both this and dynamic programming solution have time complexity of O(n) - I don't take sorting into account - but the last solution just uses a few variables, so it has very small memory complexity compared to cache solution. Fibonacci sequence grows exponentially so that cache would not be that big, but still we can avoid it.

### Count words
That's a much simpler task compared to the fibonacci/CSV task.

Once the function gets the list of matches of words out of the regex engine it passes it into the count_words function, which:

a. Turns all the words lowercase.
b. Creates defaultdict, to avoid dealing with non existent keys.
c. Iterating though every word and increasing its count in the dictionary.
d. Returning the dictionary to the main lambda_handler() function.

Then lambda_handler function creates the bytes object and uploads it to the bucket using the boto3 library.

### Response and edge cases
When everything goes smoothly lambda function returns 200 response through the API gateway.

When there is no post data (and no body in the event object) lambda function early-returns 400 response and does not save any files in the bucket.

If the input does not contain any numbers or integers, just the words are counted but both files are saved in the bucket: word count JSON file and a CSV file just with the header(names of the columns).

The opposite is also true if just numbers are provided without any words: CSV file is saved along with an empty {} JSON file.

#### Non latin input
Because matching pattern for regex is set to '\u00BF-\u1FFF\u2C00-\uD7FF' in addition to 'A-Za-z' regex engine should match words from most languages and not break words at special letters. It is tested to match Polish.

### Testing and Input
I tested all kinds of input.
I used postman for sending the API calls to the AWS API gateway and lambda function.
I pasted raw content as raw input, input data was not formatted as json or something like that.
