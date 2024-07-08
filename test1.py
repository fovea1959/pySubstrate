import logging
import pygame
from Substrate import Substrate


class MySubstrate(Substrate):
    surface: pygame.Surface

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logging.info("__init__ %s", self)

    def graphics_draw_fill(self, color):
        logging.info("draw_fill %s", color)
        self.surface.fill(color)

    def graphics_draw_point(self, x, y, color):
        # logging.info("draw_point %d,%d %s", x, y, color)
        self.surface.set_at((x, y), color)

    def graphics_initialize(self):
        logging.info("initialize %s %s", self.width, self.height)
        self.surface = pygame.display.set_mode((self.width, self.height))


def main():
    logging.basicConfig(level=logging.DEBUG)

    pygame.init()

    substrate = MySubstrate(height=400, width=400, bg_color=(255, 255, 255), max_num=10)
    substrate.wireframe = True
    substrate.seed = (3, (2147483648, 1442695824, 101364097, 3057721792, 3062170410, 3091104413, 2760727681, 761541256, 386853220, 370231422, 2888113113, 1737979786, 1172229833, 2358083335, 3545231865, 2495560810, 815527029, 1408458863, 2454089966, 2374416912, 2419746730, 888390789, 2308688895, 3234500995, 478680067, 824089314, 1844142228, 2752288477, 2203054945, 2348850365, 3421727037, 3361112599, 1081032145, 75946943, 1157211638, 4155590772, 3421806444, 3185444467, 1972829741, 650403046, 2155393369, 3221558754, 1436329122, 604267845, 13807036, 4017891941, 1715272802, 1292683371, 3588595833, 3351096949, 1826919588, 3432454215, 397223762, 3037084308, 3552368984, 3909655119, 2366250656, 1690765239, 2877733880, 241948501, 3615690006, 1657508205, 1878737975, 782075624, 2055107732, 708137062, 3691267272, 4137501711, 988240753, 2535972890, 890621310, 1626961549, 3669218499, 2888367584, 1116203983, 3729005075, 336554414, 572494560, 1632594705, 1286810099, 1916548452, 3475488520, 4033868837, 645994692, 329337290, 370016035, 577295323, 2949523846, 3142532177, 2217996610, 4133736665, 1639262768, 1940139875, 3214668641, 4240149983, 55381502, 1336393004, 3464263697, 3385925545, 3570614247, 132337697, 2168363877, 1382876241, 1408543745, 2270980153, 3809899584, 3651451114, 3554408867, 1145267277, 1015576964, 4071885177, 2552705751, 3012341193, 124695063, 1323483946, 3869179800, 1813306046, 2702563889, 287973828, 1110285864, 309361387, 3369202080, 2771642160, 2827736673, 1410737828, 3298492646, 1666772631, 1032818035, 756235840, 1333250223, 728066374, 2326545607, 3124070031, 4239125064, 2182944234, 263129524, 211490701, 3508446655, 129626400, 4100044517, 4230595968, 65411512, 908338802, 676831651, 415402926, 3059847603, 2166458285, 187779156, 333227507, 2451086700, 3786822339, 3808400803, 2452530168, 790156431, 203481533, 1055889163, 2437041380, 3624555922, 2027161623, 737949963, 3388862317, 4219145763, 3653277391, 609630474, 1859893907, 3441193170, 2417541824, 2462371549, 3590575322, 2408985345, 2042366198, 4039130092, 1609783487, 735685896, 3954782755, 1941021865, 3332705160, 61148821, 2797068387, 2440547328, 90821004, 2560340219, 4239161759, 46126180, 1993672318, 1380515949, 3134396937, 2163735395, 3606005647, 3625491123, 450716968, 3252127050, 3506905631, 1317431652, 1995950490, 816270884, 746925142, 729428769, 1223742773, 715298313, 1721051988, 3207251413, 1379216029, 2583681346, 3848505526, 2224010762, 63263605, 67626818, 211058189, 2031848002, 1034076826, 1429902446, 2376021153, 391170331, 2241857091, 4241056232, 1836227646, 3813091195, 3971887474, 2099716200, 3408209835, 2750424756, 2379036100, 1031783424, 3376957562, 806097578, 3920381851, 872121484, 2804222782, 769306873, 4022600261, 3253812497, 3979476310, 2231578988, 1584822096, 3606505764, 3824761705, 140374271, 2482474090, 3027573712, 938808911, 4291649090, 3665500754, 2831374691, 3290667703, 2261161624, 2276939084, 252967882, 1496181794, 1456735087, 2073002756, 2368278881, 2176560978, 1557908051, 1580046494, 2626646987, 2882634768, 661323127, 341630743, 2610070152, 3705283977, 3835552294, 2474009088, 2484016639, 544348482, 1056837486, 4055194988, 1498257157, 1564382697, 1089583819, 1024138304, 3919348960, 2464611435, 3379099726, 2781955001, 2952493735, 3322313672, 1723324280, 3717588963, 2729001225, 2745758745, 1614144056, 217089035, 1526808727, 3042624004, 249648519, 3660186072, 3996906467, 1754614354, 1243903120, 422063364, 3783192115, 3647934635, 2360188226, 4216296790, 4222368760, 2877503470, 2279958369, 665755326, 3697400520, 1260075069, 8588311, 2498678703, 622877472, 976590734, 262509053, 4008215264, 2447116044, 1283065548, 3355000143, 1682415960, 137299009, 1561265555, 2476373450, 3460900192, 3119844135, 4234135025, 1845181003, 2461128703, 913993602, 1341022697, 1555297897, 3610881715, 4282696586, 3697070228, 2902425036, 3499698376, 1089664578, 2190431643, 2209852085, 1685001801, 3358808316, 3678816813, 88954395, 3972214645, 2567108596, 1967978566, 3467522381, 4173672287, 2404265685, 4183208454, 1365732764, 4036603278, 1247846292, 3092002712, 2829895833, 1773265916, 3374285108, 113193116, 2233121012, 3344016423, 4134869827, 3201976097, 2501609603, 4008018620, 3358845116, 3983230944, 45074998, 11803236, 1112030049, 3959462138, 243027803, 577367718, 3630134762, 2303977846, 2903935632, 1219028856, 4230869135, 100141216, 3164617815, 1934557394, 1844830668, 1258650681, 1961111836, 225457484, 965142238, 2963256469, 1449702678, 1396245769, 2763993378, 2586146595, 1399944428, 1547075555, 640720594, 3693932927, 224205795, 3474592695, 3808537022, 2809218349, 2984020095, 765549226, 2728645099, 1535158795, 3837716771, 2349809350, 3745683799, 1748910991, 3911637083, 925286782, 2959572877, 2493061688, 3202119642, 2745945751, 2732513715, 2264617802, 2566291119, 2117938757, 3654543369, 1020148172, 1973827439, 1151723639, 3315812305, 660902927, 4212893473, 2724382060, 4132643765, 478119015, 847428416, 3851670383, 4225038422, 2609692337, 4208450138, 1603014352, 2138690811, 145854968, 338301944, 2763276710, 354658791, 2528334185, 3757733668, 2683764588, 3792229467, 646725047, 447661926, 2608858209, 3721619126, 2332012082, 1673958595, 4074667454, 1306816713, 4220325106, 1469479344, 1081383126, 536051430, 22343941, 1525725524, 657477958, 2225571209, 1993927759, 152841979, 907514098, 2632663552, 2445990881, 2242320287, 4168659963, 3215177266, 4009023234, 4092416460, 991998952, 444643760, 1621650655, 3943621661, 1442447149, 1320763671, 860907446, 2558691938, 2987081967, 4167702021, 2240804384, 2569751898, 535047352, 2579306948, 3733790375, 1987932035, 296945041, 3273650955, 1058853158, 554385712, 1186121398, 1645656990, 4117351413, 3048492217, 122361706, 739493714, 692464221, 1324370191, 3922920021, 1826775886, 2194113099, 444151407, 1837746528, 4225621229, 359987565, 1041218707, 728900342, 3899121167, 2104923759, 1160621403, 607220114, 1428292979, 2047918289, 1387940544, 2738271108, 2618593138, 1474535435, 3625507134, 3095757512, 710064232, 145364543, 1714971300, 2048632558, 3488897584, 1713288738, 383262839, 165337352, 961987730, 2723672904, 3021748768, 3480897785, 2046997399, 3203872601, 2624027499, 3594290660, 1024712947, 2680473420, 2219472842, 3068507033, 3220370665, 1375846416, 2190247762, 3968411260, 687141881, 445170359, 2264732911, 2406860028, 4061014548, 3272641069, 4192263131, 1930265900, 2633397024, 3707320181, 1116842913, 3550527135, 2166957316, 1941148007, 2534225038, 2790305404, 1810827870, 836985827, 3281338203, 1371576010, 3456055982, 1831909116, 1955882126, 2179367600, 535850082, 3893739152, 3439813637, 3480632623, 4202885464, 1173862563, 1371312642, 4188240604, 1457071069, 271061326, 2526019295, 3253956701, 663561666, 1442869435, 1746258089, 702845095, 1519624778, 280085989, 613822651, 1929789870, 3904232604, 1617526359, 2109370312, 4230961853, 2793981991, 1106551511, 2630529802, 1176694373, 2963138523, 307539262, 2391427244, 2317275972, 2037341574, 2140586773, 1400118608, 3031710455, 4036201998, 3165939277, 2865486522, 4116818557, 1220999527, 1022372624, 2548845779, 2877934916, 1659041477, 3983348205, 3740634622, 1600248643, 1996679832, 3110999585, 1683435180, 4245019459, 3748700993, 3048424081, 2264638104, 3294319487, 677355023, 268176214, 3197942611, 2112433665, 3091736167, 3868521825, 3224379933, 3659677346, 1261114934, 3870322651, 1865385200, 1402226705, 2930230197, 624), None)

    need_to_exit = False
    first = True
    while not need_to_exit:
        step = first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                need_to_exit = True
            elif event.type == pygame.TEXTINPUT:
                step = True
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                pass
            else:
                pass
                # logging.debug("event %s", event)
        if step:
            # substrate.done = True
            substrate.update()
            logging.debug("------------------- %d %s", substrate.cycles, substrate.crack_list())
        first = False
        # logging.debug("updating pygame")
        pygame.display.update()



if __name__ == '__main__':
    main()
