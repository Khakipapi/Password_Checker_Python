"""
This script checks if a password has been compromised using the Pwned Passwords API.
"""
import requests
import hashlib
import sys



def request_api_data(query_char):
  url = 'https://api.pwnedpasswords.com/range/' + query_char
  response = requests.get(url)
  if response.status_code != 200:
    raise RuntimeError(f'Error fetching: {response.status_code}, check the API and try again')
  return response

def read_response(response):
  print(response.text)

def get_password_leaks_count(hashes, hash_to_check):
  # Check if the hash_to_check is in the hashes
  hashes = (line.split(':') for line in hashes.text.splitlines())
  for h, count in hashes:
    if h == hash_to_check:
      return count
  return 0

def pwn_check(password):
  # Check if the password has been compromised
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  first5_char, tail = sha1password[:5], sha1password[5:]
  response = request_api_data(first5_char)
  return get_password_leaks_count(response, tail)

def main(arg):
  for password in arg:
    count = pwn_check(password)
    if count:
      print(f'{password} was found {count} times... you should probably change your password')
    else:
      print(f'{password} was NOT found. Carry on!')

if __name__ == '__main__':
  sys.exit(main(sys.argv[1]))
