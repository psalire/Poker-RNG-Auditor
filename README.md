
# Poker Hand Auditor

This script takes a user's poker hand history and calculates proportions of card draws and hands compared to the expected values, their confidence intervals, and chi-square p-values to determine if the site's RNG is behaving as expected. These are some of the same methods as shown in iTechlabs' [example audit report](https://itechlabs.com/certification-services/rtprng-audits/), who are one of the leaders in RNG audits for casinos.

iTechlabs also uses Marsaglia's "diehard" tests which are not covered in this script but worth looking into.

## How it works

Proportion of poker hands:

| Hand       | High Card | Pair  | Two Pair | Trips | Straight | Flush | Full House | Quads  | Straight Flush |
|------------|-----------|-------|----------|-------|----------|-------|------------|--------|----------------|
| Proportion | 0.501     | 0.423 | 0.048    | 0.021 | 0.004    | 0.002 | 0.001      | 0.0002 | 0.00003        |

A good, genuine RNG will produce these proportions given a significantly large sample size. Smaller sample sizes should fit within a reasonable confidence interval. In addition, the proportion of individual cards and hole cards together (not counting suits) should be uniform distributions.

This script parses hand history files for hole and board cards and counts every drawn card, and all 5-card hands and their ranks (e.g. pair, straight, etc.). Optionally, also counts the hole card distribution and/or the distribution of all hand combinations of hole and board cards.

Final output is tables of the sample proportions compared to the expected with upper and lower confidence limits and chi-square goodness of fit test results.

## Prerequisites

- Python 3 (3.9.1)
- treys - [A poker hand evaluation library](https://github.com/ihendley/treys)
- scipy - For chi-square tests
    - [Installation directions](https://scipy.org/install.html)

## Files

```
main.py  - Main script for output
Parse.py - Parsing hand history files
```

## How to use

Locate the directory where your poker client saves hand history. Run with `python main.py "C:\path\to\your\hand_history"`. See usage below for more options.

### Site Support

Parsing is only supported for Bovada hand history currently. To add parsing for other sites, create a new class in `Parse.py` with same methods as class `Bovada`.

On Bovada, you have to manually download hand history for each game in the accounts tab of the client. It then saves the hand history on Windows to `C:\Users\username\Bovada.lv Poker\Hand History\`.

### Usage

```
usage: main.py [-h] [--allcombinations] [--onlyme] [--holecards]
               [--holecardswithsuits] [--stdev {1,2,3}] [--site {Bovada}]
               path

This script takes a user's poker hand history and calculates proportions of
card draws and hands compared to the expected values, their confidence
intervals, and chi-square p-values to determine if the site's RNG is behaving
as expected.

positional arguments:
  path                  Path to hand history directory

optional arguments:
  -h, --help            show this help message and exit
  --allcombinations     Show table for frequency of all combinations between
                        hole and board cards.
  --onlyme              Only count my hands
  --holecards           Show table for frequency of hole cards without suits
  --holecardswithsuits  Show table for frequency of hole cards with suits
                        (Long output)
  --stdev {1,2,3}       Stdev for confidence limit, so 1 for 68%, 2 for 95%,
                        and 3 for 99.7%. Default=2
  --site {Bovada}       Which site's hand history is being parsed.
                        Default=Bovada
```

### Sample output

```

---------------------------------------------------------------------------------------------------------------
                            Distribution of Hands, 99.7% Confidence Level, n=44365                             |
---------------------------------------------------------------------------------------------------------------
     Hand      |   Expected    | Expected Size |    Sample     |     Lower     |     Upper     |  Sample Size  |
---------------------------------------------------------------------------------------------------------------
   high card   |   0.501177    |     22235     |   0.285022    |   0.487838    |   0.514516    |     12645     |
     pair      |   0.422569    |     18747     |   0.440099    |   0.411964    |   0.433174    |     19525     |
   two pair    |   0.047539    |     2109      |   0.166663    |   0.040115    |   0.054963    |     7394      |
three of a kind|   0.021128    |      937      |   0.038792    |   0.010728    |   0.031528    |     1721      |
   straight    |   0.003925    |      174      |   0.031331    |   -0.001106   |   0.008956    |     1390      |
     flush     |   0.001965    |      87       |   0.020737    |   -0.002415   |   0.006345    |      920      |
  full house   |   0.001441    |      64       |   0.015868    |   -0.002848   |   0.005730    |      704      |
four of a kind |   0.000240    |      11       |   0.001285    |   -0.005915   |   0.006395    |      57       |
straight flush |   0.000015    |       1       |   0.000203    |   -0.003914   |   0.003945    |       9       |
---------------------------------------------------------------------------------------------------------------
     Total     |   0.999999    |     44365     |   1.000000    |   0.934446    |   1.065552    |     44365     |
---------------------------------------------------------------------------------------------------------------
                                    Chi-Square Goodness of Fit Test Results                                    |
---------------------------------------------------------------------------------------------------------------
                      Chi-square                       |                     41198.402441                      |
                        p-value                        |                       0.000000                        |
---------------------------------------------------------------------------------------------------------------

---------------------------------------------------------------------------------------------------------------
                    Distribution of All Hand Combinations, 99.7% Confidence Level, n=579070                    |
---------------------------------------------------------------------------------------------------------------
     Hand      |   Expected    | Expected Size |    Sample     |     Lower     |     Upper     |  Sample Size  |
---------------------------------------------------------------------------------------------------------------
   high card   |   0.501177    |    290217     |   0.494885    |   0.498375    |   0.503979    |    286573     |
     pair      |   0.422569    |    244697     |   0.426814    |   0.419588    |   0.425550    |    247155     |
   two pair    |   0.047539    |     27528     |   0.048523    |   0.043731    |   0.051347    |     28098     |
three of a kind|   0.021128    |     12235     |   0.021557    |   0.017267    |   0.024989    |     12483     |
   straight    |   0.003925    |     2273      |   0.004214    |   0.000128    |   0.007722    |     2440      |
     flush     |   0.001965    |     1138      |   0.002243    |   -0.001721   |   0.005651    |     1299      |
  full house   |   0.001441    |      834      |   0.001482    |   -0.002444   |   0.005326    |      858      |
four of a kind |   0.000240    |      139      |   0.000266    |   -0.003505   |   0.003985    |      154      |
straight flush |   0.000015    |       9       |   0.000017    |   -0.003712   |   0.003743    |      10       |
---------------------------------------------------------------------------------------------------------------
     Total     |   0.999999    |    579070     |   1.000000    |   0.967706    |   1.032293    |    579070     |
---------------------------------------------------------------------------------------------------------------
                                    Chi-Square Goodness of Fit Test Results                                    |
---------------------------------------------------------------------------------------------------------------
                      Chi-square                       |                      124.742555                       |
                        p-value                        |                       0.000000                        |
---------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------
                        Distribution of Cards, n=157174                        |
-------------------------------------------------------------------------------
     Card      |   Expected    | Expected Size |    Sample     |  Sample Size  |
-------------------------------------------------------------------------------
      2c       |   0.019231    |     3023      |   0.019399    |     3049      |
      2d       |   0.019231    |     3023      |   0.018712    |     2941      |
      2h       |   0.019231    |     3023      |   0.019176    |     3014      |
      2s       |   0.019231    |     3023      |   0.019755    |     3105      |
      3c       |   0.019231    |     3023      |   0.019323    |     3037      |
      3d       |   0.019231    |     3023      |   0.018979    |     2983      |
      3h       |   0.019231    |     3023      |   0.018871    |     2966      |
      3s       |   0.019231    |     3023      |   0.019361    |     3043      |
      4c       |   0.019231    |     3023      |   0.019310    |     3035      |
      4d       |   0.019231    |     3023      |   0.019278    |     3030      |
      4h       |   0.019231    |     3023      |   0.019316    |     3036      |
      4s       |   0.019231    |     3023      |   0.019062    |     2996      |
      5c       |   0.019231    |     3023      |   0.019653    |     3089      |
      5d       |   0.019231    |     3023      |   0.019342    |     3040      |
      5h       |   0.019231    |     3023      |   0.019221    |     3021      |
      5s       |   0.019231    |     3023      |   0.019335    |     3039      |
      6c       |   0.019231    |     3023      |   0.019577    |     3077      |
      6d       |   0.019231    |     3023      |   0.019647    |     3088      |
      6h       |   0.019231    |     3023      |   0.018896    |     2970      |
      6s       |   0.019231    |     3023      |   0.019532    |     3070      |
      7c       |   0.019231    |     3023      |   0.019348    |     3041      |
      7d       |   0.019231    |     3023      |   0.018852    |     2963      |
      7h       |   0.019231    |     3023      |   0.019195    |     3017      |
      7s       |   0.019231    |     3023      |   0.019157    |     3011      |
      8c       |   0.019231    |     3023      |   0.019144    |     3009      |
      8d       |   0.019231    |     3023      |   0.019291    |     3032      |
      8h       |   0.019231    |     3023      |   0.019100    |     3002      |
      8s       |   0.019231    |     3023      |   0.019698    |     3096      |
      9c       |   0.019231    |     3023      |   0.018985    |     2984      |
      9d       |   0.019231    |     3023      |   0.019221    |     3021      |
      9h       |   0.019231    |     3023      |   0.019991    |     3142      |
      9s       |   0.019231    |     3023      |   0.019036    |     2992      |
      Tc       |   0.019231    |     3023      |   0.019125    |     3006      |
      Td       |   0.019231    |     3023      |   0.019183    |     3015      |
      Th       |   0.019231    |     3023      |   0.019208    |     3019      |
      Ts       |   0.019231    |     3023      |   0.019602    |     3081      |
      Jc       |   0.019231    |     3023      |   0.018896    |     2970      |
      Jd       |   0.019231    |     3023      |   0.019272    |     3029      |
      Jh       |   0.019231    |     3023      |   0.019195    |     3017      |
      Js       |   0.019231    |     3023      |   0.019259    |     3027      |
      Qc       |   0.019231    |     3023      |   0.018712    |     2941      |
      Qd       |   0.019231    |     3023      |   0.018699    |     2939      |
      Qh       |   0.019231    |     3023      |   0.019214    |     3020      |
      Qs       |   0.019231    |     3023      |   0.019660    |     3090      |
      Kc       |   0.019231    |     3023      |   0.019259    |     3027      |
      Kd       |   0.019231    |     3023      |   0.019393    |     3048      |
      Kh       |   0.019231    |     3023      |   0.019189    |     3016      |
      Ks       |   0.019231    |     3023      |   0.019361    |     3043      |
      Ac       |   0.019231    |     3023      |   0.018896    |     2970      |
      Ad       |   0.019231    |     3023      |   0.018922    |     2974      |
      Ah       |   0.019231    |     3023      |   0.018941    |     2977      |
      As       |   0.019231    |     3023      |   0.019253    |     3026      |
-------------------------------------------------------------------------------
     Total     |   1.000000    |    157196     |   1.000000    |    157174     |
-------------------------------------------------------------------------------
                    Chi-Square Goodness of Fit Test Results                    |
-------------------------------------------------------------------------------
              Chi-square               |               32.396957               |
                p-value                |               0.980401                |
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
               Distribution of Hole Cards without suits, n=65236               |
-------------------------------------------------------------------------------
  Hole Cards   |   Expected    | Expected Size |    Sample     |  Sample Size  |
-------------------------------------------------------------------------------
      2 2      |   0.004525    |      295      |   0.004338    |      283      |
      2 3      |   0.012066    |      787      |   0.011895    |      776      |
      2 4      |   0.012066    |      787      |   0.011681    |      762      |
      2 5      |   0.012066    |      787      |   0.012876    |      840      |
      2 6      |   0.012066    |      787      |   0.012187    |      795      |
      2 7      |   0.012066    |      787      |   0.012141    |      792      |
      2 8      |   0.012066    |      787      |   0.012355    |      806      |
      2 9      |   0.012066    |      787      |   0.012462    |      813      |
      2 T      |   0.012066    |      787      |   0.012187    |      795      |
      2 J      |   0.012066    |      787      |   0.012278    |      801      |
      2 Q      |   0.012066    |      787      |   0.011727    |      765      |
      2 K      |   0.012066    |      787      |   0.012631    |      824      |
      2 A      |   0.012066    |      787      |   0.011420    |      745      |
      3 3      |   0.004525    |      295      |   0.004323    |      282      |
      3 4      |   0.012066    |      787      |   0.012294    |      802      |
      3 5      |   0.012066    |      787      |   0.012049    |      786      |
      3 6      |   0.012066    |      787      |   0.012570    |      820      |
      3 7      |   0.012066    |      787      |   0.012447    |      812      |
      3 8      |   0.012066    |      787      |   0.011527    |      752      |
      3 9      |   0.012066    |      787      |   0.011512    |      751      |
      3 T      |   0.012066    |      787      |   0.012248    |      799      |
      3 J      |   0.012066    |      787      |   0.011481    |      749      |
      3 Q      |   0.012066    |      787      |   0.011895    |      776      |
      3 K      |   0.012066    |      787      |   0.012049    |      786      |
      3 A      |   0.012066    |      787      |   0.011773    |      768      |
      4 4      |   0.004525    |      295      |   0.004875    |      318      |
      4 5      |   0.012066    |      787      |   0.011926    |      778      |
      4 6      |   0.012066    |      787      |   0.011435    |      746      |
      4 7      |   0.012066    |      787      |   0.011803    |      770      |
      4 8      |   0.012066    |      787      |   0.011665    |      761      |
      4 9      |   0.012066    |      787      |   0.011543    |      753      |
      4 T      |   0.012066    |      787      |   0.011696    |      763      |
      4 J      |   0.012066    |      787      |   0.012386    |      808      |
      4 Q      |   0.012066    |      787      |   0.012217    |      797      |
      4 K      |   0.012066    |      787      |   0.012095    |      789      |
      4 A      |   0.012066    |      787      |   0.012141    |      792      |
      5 5      |   0.004525    |      295      |   0.004185    |      273      |
      5 6      |   0.012066    |      787      |   0.011558    |      754      |
      5 7      |   0.012066    |      787      |   0.011941    |      779      |
      5 8      |   0.012066    |      787      |   0.012386    |      808      |
      5 9      |   0.012066    |      787      |   0.012018    |      784      |
      5 T      |   0.012066    |      787      |   0.012263    |      800      |
      5 J      |   0.012066    |      787      |   0.012324    |      804      |
      5 Q      |   0.012066    |      787      |   0.012064    |      787      |
      5 K      |   0.012066    |      787      |   0.012754    |      832      |
      5 A      |   0.012066    |      787      |   0.012263    |      800      |
      6 6      |   0.004525    |      295      |   0.004231    |      276      |
      6 7      |   0.012066    |      787      |   0.011711    |      764      |
      6 8      |   0.012066    |      787      |   0.012800    |      835      |
      6 9      |   0.012066    |      787      |   0.011987    |      782      |
      6 T      |   0.012066    |      787      |   0.012386    |      808      |
      6 J      |   0.012066    |      787      |   0.012324    |      804      |
      6 Q      |   0.012066    |      787      |   0.011481    |      749      |
      6 K      |   0.012066    |      787      |   0.012539    |      818      |
      6 A      |   0.012066    |      787      |   0.013060    |      852      |
      7 7      |   0.004525    |      295      |   0.004537    |      296      |
      7 8      |   0.012066    |      787      |   0.012079    |      788      |
      7 9      |   0.012066    |      787      |   0.011957    |      780      |
      7 T      |   0.012066    |      787      |   0.012003    |      783      |
      7 J      |   0.012066    |      787      |   0.012187    |      795      |
      7 Q      |   0.012066    |      787      |   0.012401    |      809      |
      7 K      |   0.012066    |      787      |   0.012095    |      789      |
      7 A      |   0.012066    |      787      |   0.011466    |      748      |
      8 8      |   0.004525    |      295      |   0.004384    |      286      |
      8 9      |   0.012066    |      787      |   0.012324    |      804      |
      8 T      |   0.012066    |      787      |   0.012416    |      810      |
      8 J      |   0.012066    |      787      |   0.012018    |      784      |
      8 Q      |   0.012066    |      787      |   0.012600    |      822      |
      8 K      |   0.012066    |      787      |   0.011742    |      766      |
      8 A      |   0.012066    |      787      |   0.012294    |      802      |
      9 9      |   0.004525    |      295      |   0.004461    |      291      |
      9 T      |   0.012066    |      787      |   0.011849    |      773      |
      9 J      |   0.012066    |      787      |   0.012217    |      797      |
      9 Q      |   0.012066    |      787      |   0.012416    |      810      |
      9 K      |   0.012066    |      787      |   0.012370    |      807      |
      9 A      |   0.012066    |      787      |   0.012447    |      812      |
      T T      |   0.004525    |      295      |   0.004599    |      300      |
      T J      |   0.012066    |      787      |   0.012018    |      784      |
      T Q      |   0.012066    |      787      |   0.011267    |      735      |
      T K      |   0.012066    |      787      |   0.012386    |      808      |
      T A      |   0.012066    |      787      |   0.012033    |      785      |
      J J      |   0.004525    |      295      |   0.003909    |      255      |
      J Q      |   0.012066    |      787      |   0.012324    |      804      |
      J K      |   0.012066    |      787      |   0.012003    |      783      |
      J A      |   0.012066    |      787      |   0.012263    |      800      |
      Q Q      |   0.004525    |      295      |   0.004476    |      292      |
      Q K      |   0.012066    |      787      |   0.011987    |      782      |
      Q A      |   0.012066    |      787      |   0.011727    |      765      |
      K K      |   0.004525    |      295      |   0.004369    |      285      |
      K A      |   0.012066    |      787      |   0.011742    |      766      |
      A A      |   0.004525    |      295      |   0.004231    |      276      |
-------------------------------------------------------------------------------
     Total     |   1.000000    |     65221     |   1.000000    |     65236     |
-------------------------------------------------------------------------------
                    Chi-Square Goodness of Fit Test Results                    |
-------------------------------------------------------------------------------
              Chi-square               |               71.451145               |
                p-value                |               0.925104                |
-------------------------------------------------------------------------------
```

## Interpreting Results

Above in the sample output looking at the second table showing all hand combinations, it was found that the "high card" and "pair" sample values are not within the lower and upper values of the 99.7% confidence interval. The high card sample value was below the lower, and the pair sample value was above the upper 99.7% confidence limit. This means these that sample values fall within 0.3% of the expected outcomes given the current sample size, which is extremely unusual but still not completely impossible.

However, when looking at the first table showing the actual hand distribution of the sample, it's clear that the distribution is very irregular. All hands except for four of a kind and straight fall significantly outside of the 99.7% confidence interval. In addition, the most common hand by far was a pair, not high card as is expected.

This sample shows a bad RNG algorithm. More samples are needed to reach a conclusion.
