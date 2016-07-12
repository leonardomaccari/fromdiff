
# A python "From:" email field similarity scorer and aggregator.

If you have a mailbox and you want to parse its contents, in some cases you want
to uniquely identity the people sending the emails, merging eventual variations 
of the "From" field they use, which varies depending on time, device, etc...
This code helps you doing that.

## Input & Output
It takes as input a JSON file, containing a list of "From:" fields in
the form: 

"FirstName SecondName ThirdName..." <user@domain.extension>

then it compares every field with every other for each couple of entries
and uses a string similarity algorithm to score their similarity. 
Each From is compared in multiple ways, name Vs name, name Vs user,
email Vs email ecc... each comparison yields a value ranging from 0 (not
equal) to 1 (the same). The algorithm used for string comparison is
Ratcliff-Obershelp from python difflib. The final score is the highest of the
computed ones. 

The result is a list of the similarity scores for each couple, of the kind:

```
[[[1, 'email->email'],
  ['qiotrneverwanong', 'subttibual', 'mysttfier.com'],
  ['subtriuualnevrrwaning', 'subttibual', 'recodifiod.com']],
...]
```
The example is the comparison of two random generated From fields:
* "qiotr neverwanong" <subttibual@mysttfier.com>
* "subtriuual nevrrwaning" <subttibual@recodifiod.com>

and the output must be read like:

* 1: the score
* what matches best: email->email, email->user ecc...   
* an array with the "From" stripped of any non-text char and then the two
  entries ["name", "user", "domain"], cleaned and stripped.

In the example the two lines have a 1 match because the user of the
email is the same one. 

## Files
The genlist.py file just creates a test JSON list.
The main.py file just shows how to use it.

The interactiveaggregator.py is more practically useful. It takes a JSON list,
produces the ranking, then it lets you aggregate interactively the lines that
matched better in the algorithm. Thus, you can produce a new JSON with a
dictionary of the kind 

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
