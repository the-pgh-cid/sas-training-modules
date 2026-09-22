data test;
    length text $20 first_three $3
           middle $4 from_seventh $14;
    input text :$20.;
    first_three = substr(text, 1, 3);
    middle = substr(text, 5, 4);
    from_seventh = substr(text, 7);
    datalines;
ABCDEFGHIJ
HelloWorld
SAS-to-Python
;
run;

proc print data=test noobs;
run;
