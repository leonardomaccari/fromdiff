
A python From: field similarity scorer.

If you have a list of "From:" email fields and you want to aggregate the
emails that coming from the same person, that might similar (but
different) "From:" field, this code can help you.

It takes as input a JSON file, containing a list of "From:" fields in
the form: 

"FirstName SecondName ThirdName..." <user@domain.extension>

then it compares every entry with every other entry and uses a string
similarity algorithm to score their similarity. It then outputs a list
of the similiarity score for each one, of the kind:

```
[[[1, 'emailSimilarity'],
  [['hilltckssubstruta'], 'suestrata', 'goeg.com'],
  [['infrowhillocus'], 'suestrata', 'gwng.com']],
...]
```

each From is compared in multiple ways, name Vs name, name Vs user,
email Vs email ecc... each comparison yelds a value raning from 0 (not
equal) to 1 (the same). The algorithm used is Ratcliff-Obershelp from
python difflib. The final score is the highest of the ones. 

Ouptut is:
```
 [ [1,  # the score 
  'emailSimilarity' # which is the comparison with max score (see code)
 ],
```
and then the two entries ["name", "user", "domain"], cleaned and stripped.

In the example the two lines have a 1 match because the user of the
email is the same one (modify this behavoiur if it doens't fit
your needs).

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

You can load that json in python and do what you want with it.



