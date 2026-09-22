data test;
    length first middle last $8
           name1 name2 $24;
    input first $ middle $ last $;
    name1 = cat(first, middle, last);
    name2 = catx(' ', first, middle, last);
    datalines;
John Q Public
Jane . Doe
Bob . Smith
;
run;

proc print data=test noobs;
run;
