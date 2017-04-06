-----------Preprocessing:-----------

-Removed rows with na's 
-Remove player names
-Remove draft year and last season attributes
-Convert the positions into numbers
-Convert teams to numbers
-Only train on players w/ draft year < 2013 (rookie contract expired)
-Bin AV values into quintiles to increase coverage

-----------Classifiers:-----------
-LinearSVM
-GaussianNB
-RandomForest

-----------Objective:-----------
Predict the draft and career av AV of the last draft class (2016)



-----------Problems:-----------

-Training data is very imbalanced by class (av values); this can lead to issues in training and validation.
-There aren't enough samples for each actual AV to do anything more than 1-fold cross validation correctly w/o binning
	-This means that reasonably precise estimates are outside the realm of possibility given just the current data
-Solutions: binning AV values into classes, curating a balanced training set
-Feature reduction signficantly reduces the validation scores of each model but allows for predictions of values other than '1.0'


-----------Future Considerations:-----------
-Better feature selection using the player data
-Better metrics for validation and model selection: ROC-AUC, Stratified K-folds (if not binning)
-Finding most important features
-Actually tuning the model parameters

-----------Results:-----------

	Before binning:

	10-fold cross-validation scores (draft av):
	SVM: 0.032005565987880805
	NB: 0.06501431936497812
	RF: 0.07435215975730411

	10-fold cross-validation scores (career av):
	SVM: 0.0412899721739324
	NB: 0.09498994186202343
	RF: 0.08767307797539262


	After binning to quintiles:

	10-fold cross-validation scores (draft av):
	SVM: 0.657467158938556
	NB: 0.8112754711800976
	RF: 0.6991879601029802

	10-fold cross-validation scores (career av):
	SVM: 0.7842956911886227
	NB: 0.797373072982245
	RF: 0.8115531835136144

	
	After binning to quintiles and feature reduction:

	10-fold cross-validation scores (draft av):
	SVM: 0.7774558692405844
	NB: 0.7531441254825586
	RF: 0.5250153144380184

	10-fold cross-validation scores (career av):
	SVM: 0.6373596861243493
	NB: 0.6222216561817622
	RF: 0.635673076670976

-----------2016 Draft Results:-----------

-Random forest is the only one that provides varied and interesting results
-This makes sense that it is usually one of the best out-of-the-box classifiers

-----------Random Forest:-----------

Name                   Round                  Pick                   Team                   Position               Pred. DrAV Qtl         Pred. CarAV Qtl        
Jared Goff             1                      1                      LAR                    QB                     2.0                    3.0                    
Carson Wentz           1                      2                      PHI                    QB                     1.0                    1.0                    
Joey Bosa              1                      3                      LAC                    DE                     2.0                    2.0                    
Ezekiel Elliott        1                      4                      DAL                    RB                     4.0                    4.0                    
Jalen Ramsey           1                      5                      JAX                    CB                     2.0                    2.0                    
Ronnie Stanley         1                      6                      BAL                    T                      2.0                    2.0                    
DeForest Buckner       1                      7                      SFO                    DE                     1.0                    1.0                    
Jack Conklin           1                      8                      TEN                    T                      1.0                    2.0                    
Leonard Floyd          1                      9                      CHI                    OLB                    1.0                    1.0                    
Eli Apple              1                      10                     NYG                    CB                     1.0                    1.0                    
Vernon Hargreaves      1                      11                     TAM                    CB                     1.0                    2.0                    
Sheldon Rankins        1                      12                     NOR                    DT                     2.0                    2.0                    
Laremy Tunsil          1                      13                     MIA                    T                      2.0                    2.0                    
Karl Joseph            1                      14                     OAK                    S                      1.0                    1.0                    
Corey Coleman          1                      15                     CLE                    WR                     1.0                    2.0                    
Taylor Decker          1                      16                     DET                    T                      1.0                    1.0                    
Keanu Neal             1                      17                     ATL                    SS                     1.0                    1.0                    
Ryan Kelly             1                      18                     IND                    C                      1.0                    1.0                    
Shaq Lawson            1                      19                     BUF                    DE                     1.0                    2.0                    
Darron Lee             1                      20                     NYJ                    OLB                    1.0                    2.0                    
Will Fuller            1                      21                     HOU                    WR                     1.0                    2.0                    
Josh Doctson           1                      22                     WAS                    WR                     1.0                    1.0                    
Laquon Treadwell       1                      23                     MIN                    WR                     2.0                    2.0                    
Artie Burns            1                      25                     PIT                    CB                     2.0                    2.0                    
Paxton Lynch           1                      26                     DEN                    QB                     1.0                    1.0                    
Kenny Clark            1                      27                     GNB                    DT                     1.0                    1.0                    
Joshua Garnett         1                      28                     SFO                    G                      1.0                    1.0                    
Robert Nkemdiche       1                      29                     ARI                    DT                     2.0                    2.0                    
Vernon Butler          1                      30                     CAR                    DT                     2.0                    1.0                    
Germain Ifedi          1                      31                     SEA                    G                      2.0                    1.0                    
Emmanuel Ogbah         2                      32                     CLE                    DE                     1.0                    1.0                    
Kevin Dodd             2                      33                     TEN                    DE                     1.0                    1.0                    
Hunter Henry           2                      35                     LAC                    TE                     1.0                    1.0                    
Myles Jack             2                      36                     JAX                    OLB                    1.0                    1.0                    
Chris Jones            2                      37                     KAN                    DT                     1.0                    1.0                    
Xavien Howard          2                      38                     MIA                    CB                     1.0                    1.0                    
Noah Spence            2                      39                     TAM                    DE                     1.0                    1.0                    
Sterling Shepard       2                      40                     NYG                    WR                     1.0                    1.0                    
Austin Johnson         2                      43                     TEN                    NT                     1.0                    1.0                    
Jihad Ward             2                      44                     OAK                    DE                     1.0                    1.0                    
Derrick Henry          2                      45                     TEN                    RB                     1.0                    1.0                    
A'Shawn Robinson       2                      46                     DET                    DT                     1.0                    1.0                    
Michael Thomas         2                      47                     NOR                    WR                     1.0                    1.0                    
Jason Spriggs          2                      48                     GNB                    T                      1.0                    1.0                    
Jarran Reed            2                      49                     SEA                    DT                     1.0                    2.0                    
Deion Jones            2                      52                     ATL                    OLB                    2.0                    1.0                    
Su'a Cravens           2                      53                     WAS                    OLB                    1.0                    1.0                    
Mackensie Alexander    2                      54                     MIN                    CB                     1.0                    1.0                    
Tyler Boyd             2                      55                     CIN                    WR                     1.0                    1.0                    
Cody Whitehair         2                      56                     CHI                    G                      1.0                    2.0                    
T.J. Green             2                      57                     IND                    FS                     1.0                    1.0                    
Roberto Aguayo         2                      59                     TAM                    K                      1.0                    1.0                    
Cyrus Jones            2                      60                     NWE                    CB                     1.0                    2.0                    
Vonn Bell              2                      61                     NOR                    FS                     1.0                    1.0                    
James Bradberry        2                      62                     CAR                    CB                     1.0                    1.0                    
Adam Gotsis            2                      63                     DEN                    DT                     1.0                    1.0                    
Kevin Byard            3                      64                     TEN                    S                      1.0                    1.0                    
Carl Nassib            3                      65                     CLE                    DE                     1.0                    1.0                    
Maliek Collins         3                      67                     DAL                    DT                     1.0                    1.0                    
Yannick Ngakoue        3                      69                     JAX                    DE                     1.0                    1.0                    
Darian Thompson        3                      71                     NYG                    S                      1.0                    1.0                    
Jonathan Bullard       3                      72                     CHI                    DT                     1.0                    1.0                    
Kenyan Drake           3                      73                     MIA                    RB                     1.0                    1.0                    
Shilique Calhoun       3                      75                     OAK                    DE                     1.0                    1.0                    
Shon Coleman           3                      76                     CLE                    T                      1.0                    1.0                    
Daryl Worley           3                      77                     CAR                    CB                     2.0                    1.0                    
Joe Thuney             3                      78                     NWE                    G                      1.0                    1.0                    
Isaac Seumalo          3                      79                     PHI                    G                      1.0                    1.0                    
Adolphus Washington    3                      80                     BUF                    DT                     2.0                    1.0                    
Austin Hooper          3                      81                     ATL                    TE                     1.0                    1.0                    
Le'Raven Clark         3                      82                     IND                    T                      1.0                    1.0                    
Jordan Jenkins         3                      83                     NYJ                    OLB                    1.0                    1.0                    
Kendall Fuller         3                      84                     WAS                    CB                     1.0                    2.0                    
Braxton Miller         3                      85                     HOU                    WR                     1.0                    1.0                    
Leonte Carroo          3                      86                     MIA                    WR                     1.0                    1.0                    
Nick Vigil             3                      87                     CIN                    ILB                    1.0                    1.0                    
Kyler Fackrell         3                      88                     GNB                    OLB                    1.0                    1.0                    
Javon Hargrave         3                      89                     PIT                    DT                     1.0                    1.0                    
C.J. Prosise           3                      90                     SEA                    RB                     1.0                    1.0                    
Jacoby Brissett        3                      91                     NWE                    QB                     1.0                    1.0                    
Brandon Williams       3                      92                     ARI                    CB                     1.0                    1.0                    
Cody Kessler           3                      93                     CLE                    QB                     1.0                    1.0                    
Nick Vannett           3                      94                     SEA                    TE                     1.0                    1.0                    
Graham Glasgow         3                      95                     DET                    C                      1.0                    1.0                    
Vincent Valentine      3                      96                     NWE                    DT                     1.0                    1.0                    
Rees Odhiambo          3                      97                     SEA                    G                      1.0                    1.0                    
Justin Simmons         3                      98                     DEN                    FS                     1.0                    1.0                    
Joe Schobert           4                      99                     CLE                    OLB                    1.0                    1.0                    
Connor Cook            4                      100                    OAK                    QB                     1.0                    1.0                    
Joshua Perry           4                      102                    LAC                    ILB                    1.0                    1.0                    
Sheldon Day            4                      103                    JAX                    DT                     1.0                    1.0                    
Tavon Young            4                      104                    BAL                    CB                     1.0                    2.0                    
Parker Ehinger         4                      105                    KAN                    G                      1.0                    1.0                    
Eric Murray            4                      106                    KAN                    CB                     2.0                    1.0                    
Chris Moore            4                      107                    BAL                    WR                     1.0                    1.0                    
Ryan Smith             4                      108                    TAM                    CB                     1.0                    1.0                    
B.J. Goodson           4                      109                    NYG                    OLB                    1.0                    1.0                    
Tyler Higbee           4                      110                    LAR                    TE                     1.0                    1.0                    
Miles Killebrew        4                      111                    DET                    SS                     1.0                    1.0                    
Malcolm Mitchell       4                      112                    NWE                    WR                     1.0                    1.0                    
Nick Kwiatkoski        4                      113                    CHI                    ILB                    1.0                    1.0                    
Ricardo Louis          4                      114                    CLE                    WR                     1.0                    1.0                    
De'Vondre Campbell     4                      115                    ATL                    OLB                    1.0                    1.0                    
Hassan Ridgeway        4                      116                    IND                    DT                     1.0                    1.0                    
Pharoh Cooper          4                      117                    LAR                    WR                     1.0                    1.0                    
Juston Burris          4                      118                    NYJ                    CB                     1.0                    1.0                    
Tyler Ervin            4                      119                    HOU                    RB                     1.0                    1.0                    
Willie Beavers         4                      121                    MIN                    T                      1.0                    1.0                    
Antonio Morrison       4                      125                    IND                    ILB                    1.0                    1.0                    
Demarcus Robinson      4                      126                    KAN                    WR                     1.0                    1.0                    
Evan Boehm             4                      128                    ARI                    C                      1.0                    1.0                    
Derrick Kindred        4                      129                    CLE                    FS                     1.0                    1.0                    
Alex Lewis             4                      130                    BAL                    T                      1.0                    1.0                    
Blake Martinez         4                      131                    GNB                    LB                     1.0                    1.0                    
Rashard Robinson       4                      133                    SFO                    CB                     1.0                    1.0                    
Kenneth Dixon          4                      134                    BAL                    RB                     1.0                    1.0                    
Dak Prescott           4                      135                    DAL                    QB                     1.0                    1.0                    
Devontae Booker        4                      136                    DEN                    RB                     1.0                    1.0                    
Dean Lowry             4                      137                    GNB                    DE                     1.0                    2.0                    
Seth Devalve           4                      138                    CLE                    TE                     1.0                    1.0                    
Cardale Jones          4                      139                    BUF                    QB                     1.0                    1.0                    
Tajae Sharpe           5                      140                    TEN                    WR                     1.0                    1.0                    
Zack Sanchez           5                      141                    CAR                    CB                     1.0                    1.0                    
Ronald Blair           5                      142                    SFO                    DE                     1.0                    1.0                    
DeAndre Washington     5                      143                    OAK                    RB                     1.0                    1.0                    
John Theus             5                      145                    SFO                    T                      1.0                    1.0                    
Quinton Jefferson      5                      147                    SEA                    DT                     1.0                    2.0                    
Caleb Benenoch         5                      148                    TAM                    T                      1.0                    1.0                    
Paul Perkins           5                      149                    NYG                    RB                     1.0                    1.0                    
Jordan Howard          5                      150                    CHI                    RB                     1.0                    1.0                    
Joe Dahl               5                      151                    DET                    G                      1.0                    1.0                    
Matthew Ioannidis      5                      152                    WAS                    DT                     1.0                    1.0                    
Wendell Smallwood      5                      153                    PHI                    RB                     1.0                    1.0                    
Jordan Payton          5                      154                    CLE                    WR                     1.0                    1.0                    
Joe Haeg               5                      155                    IND                    T                      1.0                    1.0                    
Jonathan Williams      5                      156                    BUF                    RB                     1.0                    1.0                    
Brandon Shell          5                      158                    NYJ                    T                      1.0                    1.0                    
K.J. Dillon            5                      159                    HOU                    S                      1.0                    1.0                    
Kentrell Brothers      5                      160                    MIN                    OLB                    1.0                    1.0                    
Trevor Davis           5                      163                    GNB                    WR                     1.0                    1.0                    
Halapoulivaati Vaitai  5                      164                    PHI                    T                      2.0                    1.0                    
Tyreek Hill            5                      165                    KAN                    WR                     1.0                    1.0                    
D.J. Reader            5                      166                    HOU                    NT                     1.0                    1.0                    
Spencer Drango         5                      168                    CLE                    G                      1.0                    1.0                    
Antwione Williams      5                      169                    DET                    LB                     1.0                    1.0                    
Cole Toner             5                      170                    ARI                    T                      1.0                    1.0                    
Alex Collins           5                      171                    SEA                    RB                     1.0                    1.0                    
Rashard Higgins        5                      172                    CLE                    WR                     1.0                    1.0                    
Trey Caldwell          5                      173                    CLE                    DB                     1.0                    1.0                    
Jatavis Brown          5                      175                    LAC                    OLB                    1.0                    1.0                    
Andy Janovich          6                      176                    DEN                    FB                     1.0                    1.0                    
Temarrick Hemingway    6                      177                    LAR                    TE                     1.0                    1.0                    
D.J. White             6                      178                    KAN                    CB                     1.0                    1.0                    
Drew Kaser             6                      179                    LAC                    P                      1.0                    1.0                    
Jerell Adams           6                      184                    NYG                    TE                     1.0                    1.0                    
Jakeem Grant           6                      186                    MIA                    WR                     1.0                    1.0                    
David Morgan           6                      188                    MIN                    TE                     1.0                    1.0                    
Anthony Brown          6                      189                    DAL                    CB                     1.0                    1.0                    
Sebastian Tretola      6                      193                    TEN                    G                      1.0                    1.0                    
Cory James             6                      194                    OAK                    OLB                    1.0                    1.0                    
Derek Watt             6                      198                    LAC                    FB                     1.0                    1.0                    
Cody Core              6                      199                    CIN                    WR                     1.0                    1.0                    
Kyle Murphy            6                      200                    GNB                    T                      1.0                    2.0                    
Anthony Zettel         6                      202                    DET                    DT                     1.0                    1.0                    
Dadi Nicolas           6                      203                    KAN                    DE                     1.0                    1.0                    
Jordan Lucas           6                      204                    MIA                    SS                     1.0                    1.0                    
Mike Thomas            6                      206                    LAR                    WR                     1.0                    1.0                    
Kavon Frazier          6                      212                    DAL                    SS                     1.0                    1.0                    
Aaron Burbridge        6                      213                    SFO                    WR                     1.0                    1.0                    
Elandon Roberts        6                      214                    NWE                    ILB                    1.0                    1.0                    
Joey Hunt              6                      215                    SEA                    C                      1.0                    1.0                    
Kevon Seymour          6                      218                    BUF                    CB                     1.0                    1.0                    
Will Parks             6                      219                    DEN                    S                      1.0                    1.0                    
Ted Karras             6                      221                    NWE                    G                      1.0                    1.0                    
Aaron Wallace          7                      222                    TEN                    OLB                    1.0                    1.0                    
Stephen Weatherly      7                      227                    MIN                    OLB                    1.0                    1.0                    
Riley Dixon            7                      228                    DEN                    P                      1.0                    1.0                    
Demarcus Ayers         7                      229                    PIT                    WR                     1.0                    1.0                    
Daniel Braverman       7                      230                    CHI                    WR                     1.0                    1.0                    
Thomas Duarte          7                      231                    MIA                    TE                     1.0                    1.0                    
Jalen Mills            7                      233                    PHI                    FS                     1.0                    1.0                    
Vadal Alexander        7                      234                    OAK                    G                      1.0                    1.0                    
Lac Edwards            7                      235                    NYJ                    P                      1.0                    1.0                    
Dwayne Washington      7                      236                    DET                    RB                     1.0                    1.0                    
Daniel Lasco           7                      237                    NOR                    RB                     1.0                    1.0                    
Trevor Bates           7                      239                    IND                    LB                     1.0                    1.0                    
Charone Peake          7                      241                    NYJ                    WR                     1.0                    1.0                    
Jayron Kearse          7                      244                    MIN                    S                      1.0                    1.0                    
Clayton Fejedelem      7                      245                    CIN                    S                      1.0                    1.0                    
Tyler Matakevich       7                      246                    PIT                    OLB                    1.0                    1.0                    
Austin Blythe          7                      248                    IND                    C                      1.0                    1.0                    
Prince Charles Iworah  7                      249                    SFO                    CB                     1.0                    1.0                    
Kalan Reed             7                      253                    TEN                    CB                     2.0                    1.0  


-----------Naive Bayes:-----------

Name                   Round                  Pick                   Team                   Position               Pred. DrAV Qtl         Pred. CarAV Qtl        
Jared Goff             1                      1                      LAR                    QB                     2.0                    2.0                    
Carson Wentz           1                      2                      PHI                    QB                     1.0                    2.0                    
Joey Bosa              1                      3                      LAC                    DE                     2.0                    2.0                    
Ezekiel Elliott        1                      4                      DAL                    RB                     2.0                    2.0                    
Jalen Ramsey           1                      5                      JAX                    CB                     2.0                    2.0                    
Ronnie Stanley         1                      6                      BAL                    T                      1.0                    2.0                    
DeForest Buckner       1                      7                      SFO                    DE                     2.0                    2.0                    
Jack Conklin           1                      8                      TEN                    T                      2.0                    2.0                    
Leonard Floyd          1                      9                      CHI                    OLB                    1.0                    1.0                    
Eli Apple              1                      10                     NYG                    CB                     2.0                    2.0                    
Vernon Hargreaves      1                      11                     TAM                    CB                     2.0                    2.0                    
Sheldon Rankins        1                      12                     NOR                    DT                     2.0                    2.0                    
Laremy Tunsil          1                      13                     MIA                    T                      1.0                    2.0                    
Karl Joseph            1                      14                     OAK                    S                      1.0                    2.0                    
Corey Coleman          1                      15                     CLE                    WR                     1.0                    2.0                    
Taylor Decker          1                      16                     DET                    T                      1.0                    2.0                    
Keanu Neal             1                      17                     ATL                    SS                     2.0                    2.0                    
Ryan Kelly             1                      18                     IND                    C                      1.0                    2.0                    
Shaq Lawson            1                      19                     BUF                    DE                     1.0                    2.0                    
Darron Lee             1                      20                     NYJ                    OLB                    2.0                    2.0                    
Will Fuller            1                      21                     HOU                    WR                     1.0                    2.0                    
Josh Doctson           1                      22                     WAS                    WR                     1.0                    1.0                    
Laquon Treadwell       1                      23                     MIN                    WR                     2.0                    4.0                    
Artie Burns            1                      25                     PIT                    CB                     2.0                    2.0                    
Paxton Lynch           1                      26                     DEN                    QB                     1.0                    2.0                    
Kenny Clark            1                      27                     GNB                    DT                     2.0                    2.0                    
Joshua Garnett         1                      28                     SFO                    G                      2.0                    2.0                    
Robert Nkemdiche       1                      29                     ARI                    DT                     1.0                    2.0                    
Vernon Butler          1                      30                     CAR                    DT                     1.0                    2.0                    
Germain Ifedi          1                      31                     SEA                    G                      2.0                    2.0                    
Emmanuel Ogbah         2                      32                     CLE                    DE                     1.0                    2.0                    
Kevin Dodd             2                      33                     TEN                    DE                     1.0                    1.0                    
Hunter Henry           2                      35                     LAC                    TE                     1.0                    2.0                    
Myles Jack             2                      36                     JAX                    OLB                    2.0                    2.0                    
Chris Jones            2                      37                     KAN                    DT                     1.0                    2.0                    
Xavien Howard          2                      38                     MIA                    CB                     1.0                    1.0                    
Noah Spence            2                      39                     TAM                    DE                     1.0                    2.0                    
Sterling Shepard       2                      40                     NYG                    WR                     1.0                    1.0                    
Austin Johnson         2                      43                     TEN                    NT                     1.0                    2.0                    
Jihad Ward             2                      44                     OAK                    DE                     1.0                    2.0                    
Derrick Henry          2                      45                     TEN                    RB                     1.0                    1.0                    
A'Shawn Robinson       2                      46                     DET                    DT                     1.0                    2.0                    
Michael Thomas         2                      47                     NOR                    WR                     1.0                    1.0                    
Jason Spriggs          2                      48                     GNB                    T                      1.0                    1.0                    
Jarran Reed            2                      49                     SEA                    DT                     1.0                    1.0                    
Deion Jones            2                      52                     ATL                    OLB                    1.0                    2.0                    
Su'a Cravens           2                      53                     WAS                    OLB                    2.0                    2.0                    
Mackensie Alexander    2                      54                     MIN                    CB                     1.0                    2.0                    
Tyler Boyd             2                      55                     CIN                    WR                     1.0                    2.0                    
Cody Whitehair         2                      56                     CHI                    G                      1.0                    1.0                    
T.J. Green             2                      57                     IND                    FS                     1.0                    2.0                    
Roberto Aguayo         2                      59                     TAM                    K                      1.0                    2.0                    
Cyrus Jones            2                      60                     NWE                    CB                     1.0                    2.0                    
Vonn Bell              2                      61                     NOR                    FS                     1.0                    2.0                    
James Bradberry        2                      62                     CAR                    CB                     1.0                    1.0                    
Adam Gotsis            2                      63                     DEN                    DT                     1.0                    1.0                    
Kevin Byard            3                      64                     TEN                    S                      1.0                    1.0                    
Carl Nassib            3                      65                     CLE                    DE                     1.0                    1.0                    
Maliek Collins         3                      67                     DAL                    DT                     1.0                    2.0                    
Yannick Ngakoue        3                      69                     JAX                    DE                     1.0                    2.0                    
Darian Thompson        3                      71                     NYG                    S                      1.0                    1.0                    
Jonathan Bullard       3                      72                     CHI                    DT                     1.0                    1.0                    
Kenyan Drake           3                      73                     MIA                    RB                     1.0                    1.0                    
Shilique Calhoun       3                      75                     OAK                    DE                     1.0                    1.0                    
Shon Coleman           3                      76                     CLE                    T                      1.0                    1.0                    
Daryl Worley           3                      77                     CAR                    CB                     1.0                    2.0                    
Joe Thuney             3                      78                     NWE                    G                      1.0                    1.0                    
Isaac Seumalo          3                      79                     PHI                    G                      1.0                    1.0                    
Adolphus Washington    3                      80                     BUF                    DT                     1.0                    2.0                    
Austin Hooper          3                      81                     ATL                    TE                     1.0                    1.0                    
Le'Raven Clark         3                      82                     IND                    T                      1.0                    1.0                    
Jordan Jenkins         3                      83                     NYJ                    OLB                    1.0                    1.0                    
Kendall Fuller         3                      84                     WAS                    CB                     1.0                    2.0                    
Braxton Miller         3                      85                     HOU                    WR                     1.0                    1.0                    
Leonte Carroo          3                      86                     MIA                    WR                     1.0                    1.0                    
Nick Vigil             3                      87                     CIN                    ILB                    1.0                    1.0                    
Kyler Fackrell         3                      88                     GNB                    OLB                    1.0                    1.0                    
Javon Hargrave         3                      89                     PIT                    DT                     1.0                    1.0                    
C.J. Prosise           3                      90                     SEA                    RB                     1.0                    1.0                    
Jacoby Brissett        3                      91                     NWE                    QB                     1.0                    1.0                    
Brandon Williams       3                      92                     ARI                    CB                     1.0                    1.0                    
Cody Kessler           3                      93                     CLE                    QB                     1.0                    1.0                    
Nick Vannett           3                      94                     SEA                    TE                     1.0                    1.0                    
Graham Glasgow         3                      95                     DET                    C                      1.0                    1.0                    
Vincent Valentine      3                      96                     NWE                    DT                     1.0                    1.0                    
Rees Odhiambo          3                      97                     SEA                    G                      1.0                    1.0                    
Justin Simmons         3                      98                     DEN                    FS                     1.0                    1.0                    
Joe Schobert           4                      99                     CLE                    OLB                    1.0                    1.0                    
Connor Cook            4                      100                    OAK                    QB                     1.0                    1.0                    
Joshua Perry           4                      102                    LAC                    ILB                    1.0                    1.0                    
Sheldon Day            4                      103                    JAX                    DT                     1.0                    1.0                    
Tavon Young            4                      104                    BAL                    CB                     1.0                    1.0                    
Parker Ehinger         4                      105                    KAN                    G                      1.0                    1.0                    
Eric Murray            4                      106                    KAN                    CB                     1.0                    1.0                    
Chris Moore            4                      107                    BAL                    WR                     1.0                    1.0                    
Ryan Smith             4                      108                    TAM                    CB                     1.0                    1.0                    
B.J. Goodson           4                      109                    NYG                    OLB                    1.0                    1.0                    
Tyler Higbee           4                      110                    LAR                    TE                     1.0                    1.0                    
Miles Killebrew        4                      111                    DET                    SS                     1.0                    1.0                    
Malcolm Mitchell       4                      112                    NWE                    WR                     1.0                    1.0                    
Nick Kwiatkoski        4                      113                    CHI                    ILB                    1.0                    1.0                    
Ricardo Louis          4                      114                    CLE                    WR                     1.0                    1.0                    
De'Vondre Campbell     4                      115                    ATL                    OLB                    1.0                    1.0                    
Hassan Ridgeway        4                      116                    IND                    DT                     1.0                    1.0                    
Pharoh Cooper          4                      117                    LAR                    WR                     1.0                    1.0                    
Juston Burris          4                      118                    NYJ                    CB                     1.0                    1.0                    
Tyler Ervin            4                      119                    HOU                    RB                     1.0                    1.0                    
Willie Beavers         4                      121                    MIN                    T                      1.0                    1.0                    
Antonio Morrison       4                      125                    IND                    ILB                    1.0                    1.0                    
Demarcus Robinson      4                      126                    KAN                    WR                     1.0                    1.0                    
Evan Boehm             4                      128                    ARI                    C                      1.0                    1.0                    
Derrick Kindred        4                      129                    CLE                    FS                     1.0                    1.0                    
Alex Lewis             4                      130                    BAL                    T                      1.0                    1.0                    
Blake Martinez         4                      131                    GNB                    LB                     1.0                    1.0                    
Rashard Robinson       4                      133                    SFO                    CB                     1.0                    1.0                    
Kenneth Dixon          4                      134                    BAL                    RB                     1.0                    1.0                    
Dak Prescott           4                      135                    DAL                    QB                     1.0                    1.0                    
Devontae Booker        4                      136                    DEN                    RB                     1.0                    1.0                    
Dean Lowry             4                      137                    GNB                    DE                     1.0                    1.0                    
Seth Devalve           4                      138                    CLE                    TE                     1.0                    1.0                    
Cardale Jones          4                      139                    BUF                    QB                     1.0                    1.0                    
Tajae Sharpe           5                      140                    TEN                    WR                     1.0                    1.0                    
Zack Sanchez           5                      141                    CAR                    CB                     1.0                    1.0                    
Ronald Blair           5                      142                    SFO                    DE                     1.0                    1.0                    
DeAndre Washington     5                      143                    OAK                    RB                     1.0                    1.0                    
John Theus             5                      145                    SFO                    T                      1.0                    1.0                    
Quinton Jefferson      5                      147                    SEA                    DT                     1.0                    1.0                    
Caleb Benenoch         5                      148                    TAM                    T                      1.0                    1.0                    
Paul Perkins           5                      149                    NYG                    RB                     1.0                    1.0                    
Jordan Howard          5                      150                    CHI                    RB                     1.0                    1.0                    
Joe Dahl               5                      151                    DET                    G                      1.0                    1.0                    
Matthew Ioannidis      5                      152                    WAS                    DT                     1.0                    1.0                    
Wendell Smallwood      5                      153                    PHI                    RB                     1.0                    1.0                    
Jordan Payton          5                      154                    CLE                    WR                     1.0                    1.0                    
Joe Haeg               5                      155                    IND                    T                      1.0                    1.0                    
Jonathan Williams      5                      156                    BUF                    RB                     1.0                    1.0                    
Brandon Shell          5                      158                    NYJ                    T                      1.0                    1.0                    
K.J. Dillon            5                      159                    HOU                    S                      1.0                    1.0                    
Kentrell Brothers      5                      160                    MIN                    OLB                    1.0                    1.0                    
Trevor Davis           5                      163                    GNB                    WR                     1.0                    1.0                    
Halapoulivaati Vaitai  5                      164                    PHI                    T                      1.0                    1.0                    
Tyreek Hill            5                      165                    KAN                    WR                     1.0                    1.0                    
D.J. Reader            5                      166                    HOU                    NT                     1.0                    1.0                    
Spencer Drango         5                      168                    CLE                    G                      1.0                    1.0                    
Antwione Williams      5                      169                    DET                    LB                     1.0                    1.0                    
Cole Toner             5                      170                    ARI                    T                      1.0                    1.0                    
Alex Collins           5                      171                    SEA                    RB                     1.0                    1.0                    
Rashard Higgins        5                      172                    CLE                    WR                     1.0                    1.0                    
Trey Caldwell          5                      173                    CLE                    DB                     1.0                    1.0                    
Jatavis Brown          5                      175                    LAC                    OLB                    1.0                    1.0                    
Andy Janovich          6                      176                    DEN                    FB                     1.0                    1.0                    
Temarrick Hemingway    6                      177                    LAR                    TE                     1.0                    1.0                    
D.J. White             6                      178                    KAN                    CB                     1.0                    1.0                    
Drew Kaser             6                      179                    LAC                    P                      1.0                    1.0                    
Jerell Adams           6                      184                    NYG                    TE                     1.0                    1.0                    
Jakeem Grant           6                      186                    MIA                    WR                     1.0                    1.0                    
David Morgan           6                      188                    MIN                    TE                     1.0                    1.0                    
Anthony Brown          6                      189                    DAL                    CB                     1.0                    1.0                    
Sebastian Tretola      6                      193                    TEN                    G                      1.0                    1.0                    
Cory James             6                      194                    OAK                    OLB                    1.0                    1.0                    
Derek Watt             6                      198                    LAC                    FB                     1.0                    1.0                    
Cody Core              6                      199                    CIN                    WR                     1.0                    1.0                    
Kyle Murphy            6                      200                    GNB                    T                      1.0                    1.0                    
Anthony Zettel         6                      202                    DET                    DT                     1.0                    1.0                    
Dadi Nicolas           6                      203                    KAN                    DE                     1.0                    1.0                    
Jordan Lucas           6                      204                    MIA                    SS                     1.0                    1.0                    
Mike Thomas            6                      206                    LAR                    WR                     1.0                    1.0                    
Kavon Frazier          6                      212                    DAL                    SS                     1.0                    1.0                    
Aaron Burbridge        6                      213                    SFO                    WR                     1.0                    1.0                    
Elandon Roberts        6                      214                    NWE                    ILB                    1.0                    1.0                    
Joey Hunt              6                      215                    SEA                    C                      1.0                    1.0                    
Kevon Seymour          6                      218                    BUF                    CB                     1.0                    1.0                    
Will Parks             6                      219                    DEN                    S                      1.0                    1.0                    
Ted Karras             6                      221                    NWE                    G                      1.0                    1.0                    
Aaron Wallace          7                      222                    TEN                    OLB                    1.0                    1.0                    
Stephen Weatherly      7                      227                    MIN                    OLB                    1.0                    1.0                    
Riley Dixon            7                      228                    DEN                    P                      1.0                    1.0                    
Demarcus Ayers         7                      229                    PIT                    WR                     1.0                    1.0                    
Daniel Braverman       7                      230                    CHI                    WR                     1.0                    1.0                    
Thomas Duarte          7                      231                    MIA                    TE                     1.0                    1.0                    
Jalen Mills            7                      233                    PHI                    FS                     1.0                    1.0                    
Vadal Alexander        7                      234                    OAK                    G                      1.0                    1.0                    
Lac Edwards            7                      235                    NYJ                    P                      1.0                    1.0                    
Dwayne Washington      7                      236                    DET                    RB                     1.0                    1.0                    
Daniel Lasco           7                      237                    NOR                    RB                     1.0                    1.0                    
Trevor Bates           7                      239                    IND                    LB                     1.0                    1.0                    
Charone Peake          7                      241                    NYJ                    WR                     1.0                    1.0                    
Jayron Kearse          7                      244                    MIN                    S                      1.0                    1.0                    
Clayton Fejedelem      7                      245                    CIN                    S                      1.0                    1.0                    
Tyler Matakevich       7                      246                    PIT                    OLB                    1.0                    1.0                    
Austin Blythe          7                      248                    IND                    C                      1.0                    1.0                    
Prince Charles Iworah  7                      249                    SFO                    CB                     1.0                    1.0                    
Kalan Reed             7                      253                    TEN                    CB                     1.0                    1.0  


-----------SVM:-----------

Jared Goff             1                      1                      LAR                    QB                     1.0                    1.0                    
Carson Wentz           1                      2                      PHI                    QB                     1.0                    1.0                    
Joey Bosa              1                      3                      LAC                    DE                     1.0                    2.0                    
Ezekiel Elliott        1                      4                      DAL                    RB                     1.0                    1.0                    
Jalen Ramsey           1                      5                      JAX                    CB                     1.0                    2.0                    
Ronnie Stanley         1                      6                      BAL                    T                      1.0                    1.0                    
DeForest Buckner       1                      7                      SFO                    DE                     1.0                    2.0                    
Jack Conklin           1                      8                      TEN                    T                      1.0                    1.0                    
Leonard Floyd          1                      9                      CHI                    OLB                    1.0                    1.0                    
Eli Apple              1                      10                     NYG                    CB                     1.0                    2.0                    
Vernon Hargreaves      1                      11                     TAM                    CB                     1.0                    2.0                    
Sheldon Rankins        1                      12                     NOR                    DT                     1.0                    2.0                    
Laremy Tunsil          1                      13                     MIA                    T                      1.0                    1.0                    
Karl Joseph            1                      14                     OAK                    S                      1.0                    1.0                    
Corey Coleman          1                      15                     CLE                    WR                     1.0                    1.0                    
Taylor Decker          1                      16                     DET                    T                      1.0                    1.0                    
Keanu Neal             1                      17                     ATL                    SS                     1.0                    1.0                    
Ryan Kelly             1                      18                     IND                    C                      1.0                    2.0                    
Shaq Lawson            1                      19                     BUF                    DE                     1.0                    2.0                    
Darron Lee             1                      20                     NYJ                    OLB                    1.0                    2.0                    
Will Fuller            1                      21                     HOU                    WR                     1.0                    1.0                    
Josh Doctson           1                      22                     WAS                    WR                     1.0                    1.0                    
Laquon Treadwell       1                      23                     MIN                    WR                     1.0                    1.0                    
Artie Burns            1                      25                     PIT                    CB                     1.0                    2.0                    
Paxton Lynch           1                      26                     DEN                    QB                     1.0                    1.0                    
Kenny Clark            1                      27                     GNB                    DT                     1.0                    2.0                    
Joshua Garnett         1                      28                     SFO                    G                      1.0                    2.0                    
Robert Nkemdiche       1                      29                     ARI                    DT                     1.0                    2.0                    
Vernon Butler          1                      30                     CAR                    DT                     1.0                    2.0                    
Germain Ifedi          1                      31                     SEA                    G                      1.0                    2.0                    
Emmanuel Ogbah         2                      32                     CLE                    DE                     1.0                    2.0                    
Kevin Dodd             2                      33                     TEN                    DE                     1.0                    2.0                    
Hunter Henry           2                      35                     LAC                    TE                     1.0                    1.0                    
Myles Jack             2                      36                     JAX                    OLB                    1.0                    1.0                    
Chris Jones            2                      37                     KAN                    DT                     1.0                    2.0                    
Xavien Howard          2                      38                     MIA                    CB                     1.0                    2.0                    
Noah Spence            2                      39                     TAM                    DE                     1.0                    2.0                    
Sterling Shepard       2                      40                     NYG                    WR                     1.0                    1.0                    
Austin Johnson         2                      43                     TEN                    NT                     1.0                    2.0                    
Jihad Ward             2                      44                     OAK                    DE                     1.0                    2.0                    
Derrick Henry          2                      45                     TEN                    RB                     1.0                    1.0                    
A'Shawn Robinson       2                      46                     DET                    DT                     1.0                    2.0                    
Michael Thomas         2                      47                     NOR                    WR                     1.0                    1.0                    
Jason Spriggs          2                      48                     GNB                    T                      1.0                    1.0                    
Jarran Reed            2                      49                     SEA                    DT                     1.0                    2.0                    
Deion Jones            2                      52                     ATL                    OLB                    1.0                    1.0                    
Su'a Cravens           2                      53                     WAS                    OLB                    1.0                    2.0                    
Mackensie Alexander    2                      54                     MIN                    CB                     1.0                    2.0                    
Tyler Boyd             2                      55                     CIN                    WR                     1.0                    1.0                    
Cody Whitehair         2                      56                     CHI                    G                      1.0                    1.0                    
T.J. Green             2                      57                     IND                    FS                     1.0                    2.0                    
Roberto Aguayo         2                      59                     TAM                    K                      1.0                    2.0                    
Cyrus Jones            2                      60                     NWE                    CB                     1.0                    2.0                    
Vonn Bell              2                      61                     NOR                    FS                     1.0                    2.0                    
James Bradberry        2                      62                     CAR                    CB                     1.0                    2.0                    
Adam Gotsis            2                      63                     DEN                    DT                     1.0                    1.0                    
Kevin Byard            3                      64                     TEN                    S                      1.0                    1.0                    
Carl Nassib            3                      65                     CLE                    DE                     1.0                    2.0                    
Maliek Collins         3                      67                     DAL                    DT                     1.0                    2.0                    
Yannick Ngakoue        3                      69                     JAX                    DE                     1.0                    2.0                    
Darian Thompson        3                      71                     NYG                    S                      1.0                    1.0                    
Jonathan Bullard       3                      72                     CHI                    DT                     1.0                    2.0                    
Kenyan Drake           3                      73                     MIA                    RB                     1.0                    1.0                    
Shilique Calhoun       3                      75                     OAK                    DE                     1.0                    2.0                    
Shon Coleman           3                      76                     CLE                    T                      1.0                    1.0                    
Daryl Worley           3                      77                     CAR                    CB                     1.0                    2.0                    
Joe Thuney             3                      78                     NWE                    G                      1.0                    1.0                    
Isaac Seumalo          3                      79                     PHI                    G                      1.0                    2.0                    
Adolphus Washington    3                      80                     BUF                    DT                     1.0                    2.0                    
Austin Hooper          3                      81                     ATL                    TE                     1.0                    1.0                    
Le'Raven Clark         3                      82                     IND                    T                      1.0                    1.0                    
Jordan Jenkins         3                      83                     NYJ                    OLB                    1.0                    1.0                    
Kendall Fuller         3                      84                     WAS                    CB                     1.0                    2.0                    
Braxton Miller         3                      85                     HOU                    WR                     1.0                    1.0                    
Leonte Carroo          3                      86                     MIA                    WR                     1.0                    1.0                    
Nick Vigil             3                      87                     CIN                    ILB                    1.0                    1.0                    
Kyler Fackrell         3                      88                     GNB                    OLB                    1.0                    1.0                    
Javon Hargrave         3                      89                     PIT                    DT                     1.0                    2.0                    
C.J. Prosise           3                      90                     SEA                    RB                     1.0                    1.0                    
Jacoby Brissett        3                      91                     NWE                    QB                     1.0                    1.0                    
Brandon Williams       3                      92                     ARI                    CB                     1.0                    1.0                    
Cody Kessler           3                      93                     CLE                    QB                     1.0                    1.0                    
Nick Vannett           3                      94                     SEA                    TE                     1.0                    1.0                    
Graham Glasgow         3                      95                     DET                    C                      1.0                    2.0                    
Vincent Valentine      3                      96                     NWE                    DT                     1.0                    2.0                    
Rees Odhiambo          3                      97                     SEA                    G                      1.0                    1.0                    
Justin Simmons         3                      98                     DEN                    FS                     1.0                    2.0                    
Joe Schobert           4                      99                     CLE                    OLB                    1.0                    1.0                    
Connor Cook            4                      100                    OAK                    QB                     1.0                    1.0                    
Joshua Perry           4                      102                    LAC                    ILB                    1.0                    2.0                    
Sheldon Day            4                      103                    JAX                    DT                     1.0                    2.0                    
Tavon Young            4                      104                    BAL                    CB                     1.0                    2.0                    
Parker Ehinger         4                      105                    KAN                    G                      1.0                    1.0                    
Eric Murray            4                      106                    KAN                    CB                     1.0                    2.0                    
Chris Moore            4                      107                    BAL                    WR                     1.0                    1.0                    
Ryan Smith             4                      108                    TAM                    CB                     1.0                    2.0                    
B.J. Goodson           4                      109                    NYG                    OLB                    1.0                    1.0                    
Tyler Higbee           4                      110                    LAR                    TE                     1.0                    1.0                    
Miles Killebrew        4                      111                    DET                    SS                     1.0                    1.0                    
Malcolm Mitchell       4                      112                    NWE                    WR                     1.0                    1.0                    
Nick Kwiatkoski        4                      113                    CHI                    ILB                    1.0                    1.0                    
Ricardo Louis          4                      114                    CLE                    WR                     1.0                    1.0                    
De'Vondre Campbell     4                      115                    ATL                    OLB                    1.0                    1.0                    
Hassan Ridgeway        4                      116                    IND                    DT                     1.0                    2.0                    
Pharoh Cooper          4                      117                    LAR                    WR                     1.0                    1.0                    
Juston Burris          4                      118                    NYJ                    CB                     1.0                    2.0                    
Tyler Ervin            4                      119                    HOU                    RB                     1.0                    1.0                    
Willie Beavers         4                      121                    MIN                    T                      1.0                    1.0                    
Antonio Morrison       4                      125                    IND                    ILB                    1.0                    2.0                    
Demarcus Robinson      4                      126                    KAN                    WR                     1.0                    1.0                    
Evan Boehm             4                      128                    ARI                    C                      1.0                    2.0                    
Derrick Kindred        4                      129                    CLE                    FS                     1.0                    2.0                    
Alex Lewis             4                      130                    BAL                    T                      1.0                    1.0                    
Blake Martinez         4                      131                    GNB                    LB                     1.0                    1.0                    
Rashard Robinson       4                      133                    SFO                    CB                     1.0                    2.0                    
Kenneth Dixon          4                      134                    BAL                    RB                     1.0                    1.0                    
Dak Prescott           4                      135                    DAL                    QB                     1.0                    1.0                    
Devontae Booker        4                      136                    DEN                    RB                     1.0                    1.0                    
Dean Lowry             4                      137                    GNB                    DE                     1.0                    2.0                    
Seth Devalve           4                      138                    CLE                    TE                     1.0                    1.0                    
Cardale Jones          4                      139                    BUF                    QB                     1.0                    1.0                    
Tajae Sharpe           5                      140                    TEN                    WR                     1.0                    1.0                    
Zack Sanchez           5                      141                    CAR                    CB                     1.0                    2.0                    
Ronald Blair           5                      142                    SFO                    DE                     1.0                    2.0                    
DeAndre Washington     5                      143                    OAK                    RB                     1.0                    1.0                    
John Theus             5                      145                    SFO                    T                      1.0                    1.0                    
Quinton Jefferson      5                      147                    SEA                    DT                     1.0                    2.0                    
Caleb Benenoch         5                      148                    TAM                    T                      1.0                    1.0                    
Paul Perkins           5                      149                    NYG                    RB                     1.0                    1.0                    
Jordan Howard          5                      150                    CHI                    RB                     1.0                    1.0                    
Joe Dahl               5                      151                    DET                    G                      1.0                    1.0                    
Matthew Ioannidis      5                      152                    WAS                    DT                     1.0                    2.0                    
Wendell Smallwood      5                      153                    PHI                    RB                     1.0                    1.0                    
Jordan Payton          5                      154                    CLE                    WR                     1.0                    1.0                    
Joe Haeg               5                      155                    IND                    T                      1.0                    1.0                    
Jonathan Williams      5                      156                    BUF                    RB                     1.0                    1.0                    
Brandon Shell          5                      158                    NYJ                    T                      1.0                    1.0                    
K.J. Dillon            5                      159                    HOU                    S                      1.0                    1.0                    
Kentrell Brothers      5                      160                    MIN                    OLB                    1.0                    1.0                    
Trevor Davis           5                      163                    GNB                    WR                     1.0                    1.0                    
Halapoulivaati Vaitai  5                      164                    PHI                    T                      1.0                    1.0                    
Tyreek Hill            5                      165                    KAN                    WR                     1.0                    1.0                    
D.J. Reader            5                      166                    HOU                    NT                     1.0                    1.0                    
Spencer Drango         5                      168                    CLE                    G                      1.0                    1.0                    
Antwione Williams      5                      169                    DET                    LB                     1.0                    1.0                    
Cole Toner             5                      170                    ARI                    T                      1.0                    1.0                    
Alex Collins           5                      171                    SEA                    RB                     1.0                    1.0                    
Rashard Higgins        5                      172                    CLE                    WR                     1.0                    1.0                    
Trey Caldwell          5                      173                    CLE                    DB                     1.0                    2.0                    
Jatavis Brown          5                      175                    LAC                    OLB                    1.0                    1.0                    
Andy Janovich          6                      176                    DEN                    FB                     1.0                    1.0                    
Temarrick Hemingway    6                      177                    LAR                    TE                     1.0                    1.0                    
D.J. White             6                      178                    KAN                    CB                     1.0                    2.0                    
Drew Kaser             6                      179                    LAC                    P                      1.0                    1.0                    
Jerell Adams           6                      184                    NYG                    TE                     1.0                    1.0                    
Jakeem Grant           6                      186                    MIA                    WR                     1.0                    1.0                    
David Morgan           6                      188                    MIN                    TE                     1.0                    1.0                    
Anthony Brown          6                      189                    DAL                    CB                     1.0                    2.0                    
Sebastian Tretola      6                      193                    TEN                    G                      1.0                    1.0                    
Cory James             6                      194                    OAK                    OLB                    1.0                    1.0                    
Derek Watt             6                      198                    LAC                    FB                     1.0                    1.0                    
Cody Core              6                      199                    CIN                    WR                     1.0                    1.0                    
Kyle Murphy            6                      200                    GNB                    T                      1.0                    1.0                    
Anthony Zettel         6                      202                    DET                    DT                     1.0                    1.0                    
Dadi Nicolas           6                      203                    KAN                    DE                     1.0                    1.0                    
Jordan Lucas           6                      204                    MIA                    SS                     1.0                    1.0                    
Mike Thomas            6                      206                    LAR                    WR                     1.0                    1.0                    
Kavon Frazier          6                      212                    DAL                    SS                     1.0                    1.0                    
Aaron Burbridge        6                      213                    SFO                    WR                     1.0                    1.0                    
Elandon Roberts        6                      214                    NWE                    ILB                    1.0                    1.0                    
Joey Hunt              6                      215                    SEA                    C                      1.0                    2.0                    
Kevon Seymour          6                      218                    BUF                    CB                     1.0                    2.0                    
Will Parks             6                      219                    DEN                    S                      1.0                    1.0                    
Ted Karras             6                      221                    NWE                    G                      1.0                    1.0                    
Aaron Wallace          7                      222                    TEN                    OLB                    1.0                    1.0                    
Stephen Weatherly      7                      227                    MIN                    OLB                    1.0                    1.0                    
Riley Dixon            7                      228                    DEN                    P                      1.0                    1.0                    
Demarcus Ayers         7                      229                    PIT                    WR                     1.0                    1.0                    
Daniel Braverman       7                      230                    CHI                    WR                     1.0                    1.0                    
Thomas Duarte          7                      231                    MIA                    TE                     1.0                    1.0                    
Jalen Mills            7                      233                    PHI                    FS                     1.0                    1.0                    
Vadal Alexander        7                      234                    OAK                    G                      1.0                    1.0                    
Lac Edwards            7                      235                    NYJ                    P                      1.0                    1.0                    
Dwayne Washington      7                      236                    DET                    RB                     1.0                    1.0                    
Daniel Lasco           7                      237                    NOR                    RB                     1.0                    1.0                    
Trevor Bates           7                      239                    IND                    LB                     1.0                    1.0                    
Charone Peake          7                      241                    NYJ                    WR                     1.0                    1.0                    
Jayron Kearse          7                      244                    MIN                    S                      1.0                    1.0                    
Clayton Fejedelem      7                      245                    CIN                    S                      1.0                    1.0                    
Tyler Matakevich       7                      246                    PIT                    OLB                    1.0                    1.0                    
Austin Blythe          7                      248                    IND                    C                      1.0                    1.0                    
Prince Charles Iworah  7                      249                    SFO                    CB                     1.0                    2.0                    
Kalan Reed             7                      253                    TEN                    CB                     1.0                    2.0