
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


l0 = [3,0,6,1,2,4,5]
l1 = [0, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 16, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
      56, 57, 58, 1980, 1989, 2000, 2008, 2015, 2018, 2019, 2020, 2021, 2022]

l2 = [-3,-2,0,1,2,3,4,5,6]
l3 = [8, 8, 8, 8, 8, 8, 8]
l4 = []
l5 = [-10]
l6 = [-1,10]
l7 = [-1,0]
l8 = [-1,0, 21]
l9 = [880831379899970646053558729988579234456913330153760309328124858158886643077890113852386470615726945667558880086588624767580943752349815097022155951060156018129408784874658905396963956313602924001237254906679879809471957619197330842212632627921355525119616631887440832627430153939032280351825299229007692076240888798939515549385841668122331276855289688824358279031107436208700561040222904949633210734068658606065797923624038668264116422706612114355903400901494584198108172511200257135019189593506548956828047187523192158921192229072232798498512271663879541395466626440646538044663454161025433067126882513787935065641129706203676721313445591990277178134049404310097541436374176453594011552456586460882965780975476991412844518197827037828786682374410262550234752790038800074505508680024095330680981274950956673131203691423315191401850177192145018476457410307393510253429325142806254530857751919962363437924322157008507735682579889202655396479221723159022099010798301959490585059435080130444505038261678809930945405035722661899646949732635763759086069777883957301962272746297457228728336223004727693122736033466242926908756974382642657123131236376444913678755388474420131305321473456130993331954008455604660851763751750454850467878151332253493889963340143293183048656568151292085866865158358808113160657887591956465477036314540400904359558796041231860074818421176405741583679968456270120995710087617769910754709913863019881047539157982317414470122364342615946669853978417583483370309146236171017464319227085228248681556128114260167759687621214292825825820888717954634677969273174523686335523468194054233597386969802527075459442660427642365773817218037494425380539001962502840544063472386065750938776693235014525124121798836985522040388650691798677735797057038411786506188183573661656495295478988011986175414328934436509520339839235425929520708640442497383380897781639866830695667365051264668863042272531050342317167615353504411787242108418308555275868828220932465458131206241132903915938977652193209311796978699972437705337193195305263698305295438424056554952293822510391164267501567711329643768808313798999706460535587299885792344569133301537603093281248581588866430778901138523864706157269456675588800865886247675809437523498150970221559510601560181294087848746589053969639563136029240012372549066798798094719576191973308422126326279213555251196166318874408326274301539390322803518252992290076920762408887989395155493858416681223312768552896888243582790311074362087005610402229049496332107340686586060657979236240386682641164227066121143559034009014945841981081725112002571350191895935065489568280471875231921589211922290722327984985122716638795413954666264406465380446634541610254330671268825137879350656411297062036767213134455919902771781340494043100975414363741764535940115524565864608829657809754769914128445181978270378287866823744102625502347527900388000745055086800240953306809812749509566731312036914233151914018501771921450184764574103073935102534293251428062545308577519199623634379243221570085077356825798892026553964792217231590220990107983019594905850594350801304445050382616788099309454050357226618996469497326357637590860697778839573019622727462974572287283362230047276931227360334662429269087569743826426571231312363764449136787553884744201313053214734561309933319540084556046608517637517504548504678781513322534938899633401432931830486565681512920858668651583588081131606578875919564654770363145404009043595587960412318600748184211764057415836799684562701209957100876177699107547099138630198810475391579823174144701223643426159466698539784175834833703091462361710174643192270852282486815561281142601677596876212142928258258208887179546346779692731745236863355234681940542335973869698025270754594426604276423657738172180374944253805390019625028405440634723860657509387766932350145251241217988369855220403886506917986777357970570384117865061881835736616564952954789880119861754143289344365095203398392354259295207086404424973833808977816398668306956673650512646688630422725310503423171676153535044117872421084183085552758688282209324654581312062411329039159389776521932093117969786999724377053371931953052636983052954384240565549522938225103911642675015677113296437688083137989997064605355872998857923445691333015376030932812485815888664307789011385238647061572694566755888008658862476758094375234981509702215595106015601812940878487465890539696395631360292400123725490667987980947195761919733084221263262792135552511961663188744083262743015393903228035182529922900769207624088879893951554938584166812233127685528968882435827903110743620870056104022290494963321073406865860606579792362403866826411642270661211435590340090149458419810817251120025713501918959350654895682804718752319215892119222907223279849851227166387954139546662644064653804466345416102543306712688251378793506564112970620367672131344559199027717813404940431009754143637417645359401155245658646088296578097547699141284451819782703782878668237441026255023475279003880007450550868002409533068098127495095667313120369142331519140185017719214501847645741030739351025342932514280625453085775191996236343792432215700850773568257988920265539647922172315902209901079830195949058505943508013044450503826167880993094540503572266189964694973263576375908606977788395730196227274629745722872833622300472769312273603346624292690875697438264265712313123637644491367875538847442013130532147345613099333195400845560466085176375175045485046787815133225349388996334014329318304865656815129208586686515835880811316065788759195646547703631454040090435955879604123186007481842117640574158367996845627012099571008761776991075470991386301988104753915798231741447012236434261594666985397841758348337030914623617101746431922708522824868155612811426016775968762121429282582582088871795463467796927317452368633552346819405423359738696980252707545944266042764236577381721803749442538053900196250284054406347238606575093877669323501452512412179883698552204038865069179867773579705703841178650618818357366165649529547898801198617541432893443650952033983923542592952070864044249738338089778163986683069566736505126466886304227253105034231716761535350441178724210841830855527586882822093246545813120624113290391593897765219320931179697869997243770533719319530526369830529543842405655495229382251039116426750156771132964376]
l10 = [-1,0,1]

print(fibonacci_process(l0))
print(fibonacci_process(l1))
print(fibonacci_process(l2))
print(fibonacci_process(l3))
print(fibonacci_process(l4))
print(fibonacci_process(l5))
print(fibonacci_process(l6))
print(fibonacci_process(l7))
print(fibonacci_process(l8))
print(fibonacci_process(l9))
print(fibonacci_process(l10))
# print(fibonacci_process([-10]))