from fsp.models import (User,Point,FoodAvailable,Order,Bonus)
from fsp import db, bcrypt
from datetime import date

"Here, the info data for each models defined in models.py have been defined ready to be added in database"

def fill_database():

    Nicola_Menga = User(id=1, first_name='Nicola', last_name='Menga',
                              email='s287975@studenti.polito.it',phone=3888809809,
                              password=bcrypt.generate_password_hash('nicola').decode('utf-8'),volunteer=True,bonus=600)

    Mohammed_Maataoui = User(id=2, first_name='Mohammed', last_name='Maataoui',
                            email='s289380@studenti.polito.it', phone=384678437,
                            password=bcrypt.generate_password_hash('mohammed').decode('utf-8'),
                            volunteer=True,bonus=600
                           )

    Tommaso_Caroli = User(id=3, first_name='Tommaso', last_name='Caroli',phone=3854784337,
                          email='s282534@studenti.polito.it', password=bcrypt.generate_password_hash('tommaso').decode('utf-8'),volunteer=True,bonus=600)

    Mariangela_Avantaggiato = User(id=4, first_name='Mariangela', last_name='Avantaggiato',phone=384784337,
                          email='s287946@studenti.polito.it', password=bcrypt.generate_password_hash('mariangela').decode('utf-8'),volunteer=True,bonus=600)

    Muhammad_Ali = User(id=5, first_name='Muhammad', last_name='Ali',phone=384784337,
                          email='s289226@studenti.polito.it', password=bcrypt.generate_password_hash('muhammad').decode('utf-8'),volunteer=True,bonus=600)

    Doaaelrhman_Ali = User(id=6, first_name='Doaaelrhman', last_name='Ali',phone=384784337,
                          email='s289604@studenti.polito.it', password=bcrypt.generate_password_hash('doaaelrhman').decode('utf-8'),volunteer=True,bonus=600)


    db.session.add_all([Nicola_Menga,Mohammed_Maataoui,Tommaso_Caroli,Mariangela_Avantaggiato,Muhammad_Ali,Doaaelrhman_Ali])

    # Food Sharing Points-(sup based)---------------------------------------------------------------------------------------------

    auchan = Point(id=1, name='Auchan', city='Turin',
                        address='Corso Romania, 460')

    coop = Point(id=2, name='Coop', city='Turin',
                        address='Corso Belgio, 151/d')

    carrefour = Point(id=3, name='Carrefour', city='Turin',
                        address='Corso Monte Cucco, 108')
    esselunga = Point(id=4, name='Esselunga', city='Turin',
                        address='Corso Traiano, 131')



    db.session.add_all(
        [auchan,coop,carrefour,esselunga])

    #---------------------------------------------------------------------------

    pasta1 = FoodAvailable(id=1,  type='Penne_Barilla',expired_data=date(2020, 1, 22), point='Auchan',availability=4)
    pasta2 = FoodAvailable(id=2, type='Lasagne_Divella', expired_data=date(2020, 1, 18), point='Coop', availability=5)
    pasta3 = FoodAvailable(id=3, type='Farfalle_Emiliane', expired_data=date(2020, 1, 29), point='Carrefour', availability=1)
    pasta4 = FoodAvailable(id=4, type='Fusilli_Garofalo', expired_data=date(2020, 2, 1), point='Esselunga', availability=2)
    latte1 = FoodAvailable(id=5, type='Latte_Parmalat', expired_data=date(2020, 1, 22), point='Auchan', availability=4)
    latte2 = FoodAvailable(id=6, type='Latte_Zymil', expired_data=date(2020, 1, 18), point='Coop', availability=6)
    passata1 = FoodAvailable(id=7, type='Passata_Pomi', expired_data=date(2020, 1, 21), point='Carrefour', availability=3)
    pelati = FoodAvailable(id=8, type='Pelati_Cirio', expired_data=date(2020, 2, 22), point='Esselunga',availability=2)
    tonno1 = FoodAvailable(id=9, type='Tonno_Callipo', expired_data=date(2020, 1, 26), point='Auchan', availability=4)
    farina1 = FoodAvailable(id=10, type='Farina00_Barilla', expired_data=date(2020, 1, 17), point='Coop', availability=3)
    biscotti1 = FoodAvailable(id=11, type='Macine_MulinoBianco', expired_data=date(2020, 1, 19), point='Carrefour', availability=3)
    caffe1 = FoodAvailable(id=12, type='Caffe_Lavazza', expired_data=date(2020, 2, 2), point='Esselunga',availability=2)
    caffe2 = FoodAvailable(id=13,  type='Caffe_Mauro',expired_data=date(2020, 1, 20),point='Coop',availability=1)
    yogurt1 = FoodAvailable(id=14,  type='Skyr_Danone',expired_data=date(2020, 1, 20),point='Carrefour',availability=7)
    yogurt2 = FoodAvailable(id=15, type='Yogurt_Vitasnella', expired_data=date(2020, 1, 17), point='Auchan', availability=3)

    db.session.add_all([pasta1,pasta2,pasta3,pasta4,latte1,latte2,passata1,pelati,tonno1,farina1,biscotti1,caffe1,caffe2,yogurt1,yogurt2])

    # Orders----------------------------------------------------------------------------------------------------
    order1 = Order(id=1, date_order=date(2018, 12, 26),date_order_done=date(2018, 12, 25), user_id=2, point='Carrefour')
    order2 = Order(id=2, date_order=date(2019, 8, 20),date_order_done=date(2019, 6, 16), user_id=1, point='Auchan')
    order3 = Order(id=3, date_order=date(2018, 9, 26),date_order_done=date(2018, 7, 25), user_id=3, point='Coop')
    order4 = Order(id=4, date_order=date(2019, 10, 20),date_order_done=date(2019, 8, 16), user_id=4, point='Esselunga')
    order5 = Order(id=5, date_order=date(2018, 7, 26),date_order_done=date(2018, 5, 25), user_id=5, point='Carrefour')
    order6 = Order(id=6, date_order=date(2019, 6, 20),date_order_done=date(2019, 4, 16), user_id=6, point='Coop')


    db.session.add_all([order1,order2,order3,order4,order5,order6])

    bonus1 = Bonus(id=1, date_bonus=date(2018, 12, 25),bonus=520,voucher=None,user_id=1)
    bonus2 = Bonus(id=2, date_bonus=date(2020, 01, 25),bonus=-400,voucher=2,user_id=5)
    bonus3 = Bonus(id=3, date_bonus=date(2020, 01, 1), bonus=230, voucher=None, user_id=2)
    bonus4 = Bonus(id=4, date_bonus=date(2019, 01, 25), bonus=-200, voucher=1, user_id=4)
    bonus5 = Bonus(id=5, date_bonus=date(2018, 01, 25), bonus=120, voucher=None, user_id=3)
    bonus6 = Bonus(id=6, date_bonus=date(2018, 01, 25), bonus=150, voucher=None, user_id=6)


    db.session.add_all([bonus1,bonus2,bonus3,bonus4,bonus5,bonus6])

    db.session.commit()


