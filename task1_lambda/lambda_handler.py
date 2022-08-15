import json
import re
from datetime import datetime
from collections import defaultdict
import boto3

def numbers_to_csv_string(numbers: list[int]):

    output = 'previos Fibonacci number,observed number,nex Fibonacci number\n'

    # edge case - list is empty -> output is just the header (column names)
    if len(numbers) == 0:
        return output

    # pointer for going through numbers list
    left = 0

    # checking and processing negative numbers (assuming we didn't reach the end of the numbers list)
    while left < len(numbers) and numbers[left] < 0:

        # adding string consisting of the number surrounded by comas with line break at the end
        # to the end of output variable
        output += ',' + str(numbers[left]) + ',\n'
        left += 1

    # if current number is 0 (assuming we didn't reach the end of the numbers list)
    if left < len(numbers) and numbers[left] == 0:
        output += ',0,1\n'
        left += 1

    # if current number is 1 (assuming we didn't reach the end of the numbers list)
    if left < len(numbers) and numbers[left] == 1:
        output += '0,1,1\n'
        left += 1

    # setting up the prev, current and nex variables (to store previous, current and next number in the sequence
    # respectively
    prev = 1
    current = 1
    nex = prev + current

    # going through the numbers from where we left off with the left pointer
    for n in numbers[left:]:

        # if n is bigger then current number in the fibonacci sequence, generate new number in the sequence by adding
        # two previous numbers, eventually n will equal to a fib number or be larger than it
        while n > current:
            prev, current = current, current + prev
            nex = current + prev

        # n equals to a fibonacci number exactly
        # add prev, current and next with comas between as a row to the output string
        if n == current:
            to_append = str(prev) + ',' + str(current) + ',' + str(nex) + '\n'
            output += to_append

        # n is smaller fibonacci number (it's in between numbers), add just current with comas around
        # as a row to the output string
        elif n < current:
            output += ',' + str(n) + ',\n'

    return output


def fibonacci_process(numbers: list):

    # checking if the list is empty - no integers/numbers found
    if len(numbers) == 0:
        return numbers_to_csv_string([])

    # I turn numbers into set to get just the unique numbers as it is in the example output
    # print(numbers)
    numbers = list(set(numbers))

    # convert numbers to int using list comprehension - regex returns matches as strings, in general input is usually
    # by default also a string
    numbers = [int(x) for x in numbers]
    # sort numbers list inplace
    numbers.sort()

    #convert numbers to a CSV compliant string using numbers_to_csv_string function
    output = numbers_to_csv_string(numbers)

    return output


def count_words(words: list):
    words = list(map(str.lower, words))
    word_count = defaultdict(int)

    for w in words:
        # print(w)
        word_count[w] += 1

    return word_count

def filename_now():
    now = datetime.now()
    return now.strftime("%Y_%m_%d__%H_%M_%S__%f")

def lambda_handler(event, context):

    s3 = boto3.client('s3')
    bucket = 'word-count-fibonacci-005'

    # no data in post -> body doesn't exist
    if 'body' not in event:

        transaction_response = {}
        transaction_response['message'] = 'Error, no post data'

        response_object = {}
        response_object['statusCode'] = 400
        response_object['headers'] = {}
        response_object['headers']['Content-Type'] = 'application/json'
        response_object['message'] = 'Error, no post data'
        response_object['body'] = json.dumps(transaction_response)

        return response_object

    body = event['body']
    print(event)
    print(body)

    # joining body (list) into one long string
    body = ''.join(body)

    # print(len(body))

    # Using regex I'm matching all 'digit collections' to find integers. I treat '.' as the separator as that seems to
    # be the case looking at the example input/output
    numbers = re.findall('\d+', body)

    str_csv = fibonacci_process(numbers)
    # print(str_csv)

    file_ = filename_now() + '.csv'
    byte_stream = bytes(str_csv.encode('UTF-8'))
    r = s3.put_object(Bucket=bucket, Key=file_, Body=byte_stream)
    print('s3 put integers content: ', r)

    # matching just latin letters: words = re.findall('[A-Za-z]+', body)

    # following matches unicode letters
    words = re.findall('[\u00BF-\u1FFF\u2C00-\uD7FFA-Za-z]+', body)
    words = count_words(words)

    file_ = file_[:-3] + '.json'
    byte_stream = bytes(json.dumps(words).encode('UTF-8'))
    r = s3.put_object(Bucket=bucket, Key=file_, Body=byte_stream)
    print('s3 put words content: ', r)

    transaction_response = {}

    # transaction_response['numbers'] = numbers
    # transaction_response['string_csv'] = str_csv
    # transaction_response['words'] = words
    transaction_response['message'] = 'Files generated'

    response_object = {}
    response_object['statusCode'] = 200
    response_object['headers'] = {}
    response_object['headers']['Content-Type'] = 'application/json'
    response_object['message'] = 'Hello from lambda'
    response_object['body'] = json.dumps(transaction_response)

    return response_object