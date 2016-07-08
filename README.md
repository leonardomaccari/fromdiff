
# A python "From:" email field similarity scorer.

If you have a bunch of emails and you want to identify the sender of 
the email, even if he uses slightly different "From" fields, this
code can help you.

## Input & Output
It takes as input a JSON file, containing a list of "From:" fields in
the form: 

"FirstName SecondName ThirdName..." <user@domain.extension>

then it compares every entry with every other entry and uses a string
similarity algorithm to score their similarity. It then outputs a list
of the similarity score for each one, of the kind:

```
[[[1, 'emailSimilarity'],
  [['hilltckssubstruta'], 'suestrata', 'goeg.com'],
  [['infrowhillocus'], 'suestrata', 'gwng.com']],
...]
```

each From is compared in multiple ways, name Vs name, name Vs user,
email Vs email ecc... each comparison yields a value ranging from 0 (not
equal) to 1 (the same). The algorithm used is Ratcliff-Obershelp from
python difflib. The final score is the highest of the ones. 

Output is:
```
 [ [1,  # the score 
  'emailSimilarity' # which is the comparison with max score (see code)
 ],
```
and then the two entries ["name", "user", "domain"], cleaned and stripped.

In the example the two lines have a 1 match because the user of the
email is the same one (modify this behaviour if it doesn't fit
your needs).

## Files
The genList.py file just creates a test JSON list.
The main.py file just shows how to use it.

The interactiveaggregator.py is more useful. It takes a JSON list,
produces the ranking, then it lets you aggregate interactively the lines
that matched better in the algorithm. Thus, you can produce a new JSON
with a dictionary of the kind 

```
{ 
  fromStringCopy1 : fromString,
  fromStringCopy2 : fromString,
  ...
}
```
Before saving the file it will ask you if you want to aggregate the
results and detect loops, which means that if you have chosen something
like:

```
{ 
  fromStringCopy1 : fromStringCopy2,
  fromStringCopy3 : fromString,
  ...
}
```
This will be reduced to:

```
{ 
  fromStringCopy1 : fromString,
  fromStringCopy2 : fromString,
  fromStringCopy3 : fromString,
  ...
}
```

and loops will be detected too.

You can load that JSON in python and do what you want with it.

# LICENSE: 

Copyright Leonardo Maccari

This code is released under the terms of the GPLv3 License.




