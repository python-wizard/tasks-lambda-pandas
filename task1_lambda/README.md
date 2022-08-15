Using AWS cloud create a text-analysis microservice. 

1. Create a Lambda function that extracts a text string from the request and:

    I) Finds all integers in the input text, saves them in ascending order to a csv file together with the previous and following numbers of the fibonacci sequence (if the number is a part of the sequence)

    II) Finds all words containing only alphabetical characters, counts the number of word occurrences, saves it to a json file

    III) Uploadas those two files to an s3 bucket

2. Create a private S3 bucket that will store files produced by the Lambda function.

3. Create public API endpoint: connect Lambda function to API Gateway so that text input can be sent via POST method, return 200 code if process completed successfully (files were created and uploaded to S3 bucket)


You can use AWS console for creation of AWS services
Publish the code used by the Lambda to a public github repository 
Please consider any possible corner cases, describe them and argument proposed solutions inside the README file
Present your solution during the interview

In example_io folder you will find example input text and files your function would be expected to produce.
test_diagram.png image shows the architecture of the microservice you will create.

Have fun!
