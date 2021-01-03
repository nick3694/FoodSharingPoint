from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import random
import string
from datetime import datetime
import database_info
from fds import app, db, bcrypt, mail
from fds.forms import (RegistrationForm, LoginForm, ContactForm,
                       RequestResetForm, ResetPasswordForm,CompleteOrderForm,CompleteForm,VolunteerForm,AddFood,RemoveFood,GiveBonus)
from fds.models import (User,Point,FoodAvailable,Order,Bonus)
global data

@app.before_first_request
def setup_db():
    db.drop_all()
    db.create_all()
    database_info.fill_database()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Food Sharing Point')


@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/about')
def about():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    return render_template('about.html',flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus,title='About us | FSP')


@app.route('/team')
def team():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    return render_template('team.html',flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus,title='Team | FSP')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if error_vol:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data, password=hashed_password, volunteer=False,bonus=0)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to login', 'success')
            flash('Check your email, you are part of the community!', 'info')
            send_email(user.email, 'Subscription to FSP', 'registration_email')
            return redirect(url_for('login'))
        return render_template('signup.html', title='Sign up | FSP', form=form, error=True)
    else:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                        phone=form.phone.data, password=hashed_password, volunteer=False,bonus=0)
            session['first_name'] = form.first_name.data
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to login', 'success')
            flash('Check your email, you are part of the community!', 'info')
            send_email(user.email, 'Subscription to FSP', 'registration_email')

            return redirect(url_for('login'))
        return render_template('signup.html', title='Sign up | FSP', form=form, error=False)



def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    user = User.query.filter_by(email=to).first()
    msg.html = render_template(template + '.html', user=user, **kwargs)
    mail.send(msg)


@app.route('/dashboard')
def dashboard():
    if session.get('first_name'):
        return render_template('dashboard.html')
    else:
        return redirect('signup')


@app.route('/main')
@login_required
def main():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    return render_template('main.html',flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus,title='Service Page | FSP')


@app.route('/site')
@login_required
def site():
    return render_template('site.html',bonus=current_user.bonus,flag_access_as_volunteer=flag_access_as_volunteer,title='Homepage | FSP')

flag_access_as_volunteer=False
@app.route("/login", methods=['GET', 'POST'])
def login():
    flag = 0;
    form = LoginForm()
    global flag_access_as_volunteer
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if request.form.get('d_enabled') == 'on':
            flag_access_as_volunteer=True
            if user and bcrypt.check_password_hash(user.password, form.password.data) and user.volunteer is True:
                session['email'] = form.email.data
                login_user(user)  # , remember=form.remember.data faccio il login dell'user e verifico anche il remember me
                return redirect(url_for('site'))
            else:
                flag = 1;
                flash('Login Unsuccessful. Please check email and password', 'danger')
        else:
            flag_access_as_volunteer=False
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session['email'] = form.email.data
                login_user(user)  # , remember=form.remember.data faccio il login dell'user e verifico anche il remember me
                return redirect(url_for('main'))
            else:
                flag = 1;
                flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Log in | FSP', form=form, flag=flag)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/relogin", methods=['GET', 'POST'])
def relogin():
    logout_user()
    return redirect(url_for('login'))

@app.route("/reset_password", methods=['GET', 'POST'])  # route in which we enter the email to request a password reset
def reset_request():
    # if current_user.is_authenticated:
    #    return redirect(url_for('home'))
    logout_user()
    form = RequestResetForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:  # se vuoi cambiare password quando sei loggato, puoi farlo solo se inserisci la tua password
            if current_user.email != form.email.data:
                flash('This email does not exits, try whit a different one', 'info')
                return redirect(url_for('reset_request'))
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('This email does not exits, try whit a different one', 'info')
            return redirect(url_for('reset_request'))
        send_reset_email(user, 'Request Reset Password', 'message_reset_password')
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password | FSP', form=form)


@app.route("/reset_password/<token>",
           methods=['GET', 'POST'])  # route in which we actually reset the password with the token active
def reset_token(token):
    # if current_user.is_authenticated:
    #    return redirect(url_for('home'))
    logout_user()
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! ', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password | FSP', form=form)


def send_reset_email(user, subject, template, **kwargs):
    token = user.get_reset_token()
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = ('For reset password click the following link: ' + (url_for('reset_token', token=token, _external=True)))
    mail.send(msg)


@app.route('/yourprofile')
@login_required
def yourprofile():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    return render_template('yourprofile.html',title='Your Profile | FSP' ,first_name=current_user.first_name, last_name=current_user.last_name,
                           email=current_user.email, phone=current_user.phone,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)


@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    form = ContactForm()
    success = False;
    if request.method == 'POST':
        if form.validate_on_submit() == False:
            flash('All fields are required.')
            return render_template('contactus.html',title='Leave a feedback | FSP', form=form, success=success,flag_access_as_volunteer=flag_access_as_volunteer)
        else:
            msg = Message(form.subject.data, sender='contact@example.com', recipients=['foodsharingpoint@gmail.com'])
            msg.body = """
      From: %s &lt;%s&gt;
      %s
      """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            flash("Thank you for your message. We'll get back to you shortly.")
            return render_template('contactus.html',title='Leave a feedback | FSP', form=form, success=True,flag_access_as_volunteer=flag_access_as_volunteer)

    elif request.method == 'GET':
        return render_template('contactus.html',title='Leave a feedback | FSP', form=form, success=success,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)


@app.route('/shoppingcart')
@login_required
def shoppingcart():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    points = [point.name for point in Point.query.all()]
    adresses=[point.address for point in Point.query.all()]
    supermarkets=zip(points,adresses)

    return render_template('shoppingcart.html',title='Book food | FSP',supermarkets=supermarkets,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)

food_booked=[]
quantity_booked=[]
point_selected=[]
@app.route('/foodavailable/<point>', methods=['GET', 'POST'])
def foodavailable(point):
    global point_selected
    point_selected=point
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    foodavailable = [food.type for food in FoodAvailable.query.filter_by(point=point).all()]
    dates= [food.expired_data for food in FoodAvailable.query.filter_by(point=point).all()]
    datees=[d.strftime('%Y-%m-%d') for d in dates]
    availabilities=[food.availability for food in FoodAvailable.query.filter_by(point=point).all()]
    items=[[x,unicode(y),z,u] for x,y,z,u in zip(foodavailable,datees,dates,availabilities)]
    flag_noproduct=True
    form=CompleteOrderForm()
    global food_booked
    global quantity_booked
    food_booked=[]
    quantity_booked=[]
    if form.validate_on_submit():
        today=datetime.today()
        datebook = datetime.strptime(str(form.order_date.data), '%Y-%m-%d')
        if datebook>today:
            for food,datee,datx,avail in items:
                if request.form.get(food) == 'on':
                    disp = FoodAvailable.query.filter_by(type=food,point=point_selected,expired_data=datx).first()
                    if  int(request.form.get("box_"+food)) <= int(disp.availability):
                        food_booked.append(str(food))
                        quantity_booked.append((int(request.form.get("box_"+food))))          #in order to distinguish food with the same name and different expired data
                        flag_noproduct = False
                    else:
                        food_booked=[]
                        quantity_booked=[]
                        flash("Error: one or more items are greater than available units!")
                        return render_template('foodavailable.html',title='Book food | FSP', foodavailable=foodavailable, dates=dates,availabilities=availabilities, form=form,bonus=bonus,items=items)
                else:
                    continue
            if flag_noproduct is True:
                flash("Please choose at least a product!")
                return redirect(url_for('main'))
            else:
                return render_template('gocart.html',title='Book food | FSP',form=form,cart=zip(food_booked,quantity_booked),flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)
        else:
            flash("Please choose a booking date staring from tomorrow!")
    return render_template('foodavailable.html',title='Book food | FSP',foodavailable=foodavailable,dates=dates,availabilities=availabilities,form=form,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus,items=items)

@app.route('/gocart', methods=['GET', 'POST'])
@login_required
def gocart():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    form=CompleteForm()

    if len(food_booked)==0:
        flash("Your cart is empty, please do the shopping list first! ")
        return redirect('main')
    if form.validate_on_submit:
        orderdate = form.order_date.data
        today = datetime.today()
        orderadded = Order(date_order_done=today, date_order=orderdate, user_id=current_user.id, point=point_selected)
        db.session.add(orderadded)
        for food in food_booked:
            disp = FoodAvailable.query.filter_by(type=food,point=point_selected).first()
            disp.availability = disp.availability  - int(quantity_booked[food_booked.index(food)])
            db.session.commit()
            if disp.availability==0:
                FoodAvailable.query.filter_by(type=food,point=point_selected).delete()
                db.session.commit()
        flash("Your booking has been completed successfully!"
              "We have sent you an e-mail."
              "Thank you! ")
        msg = Message(sender=app.config['MAIL_USERNAME'], recipients=[current_user.email])
        msg.body = """Dear %s %s you have required a booking on %s in %s.
        Our team will check the availability of your booking date as soon as possible, thank you!""" % (
            current_user.first_name, current_user.last_name, form.order_date.data, point_selected)
        mail.send(msg)

        return render_template('main.html',title='Service Page | FSP',success=True,bonus=bonus,flag_access_as_volunteer=flag_access_as_volunteer)
    return render_template('gocart.html',title='Book food | FSP',form=form,cart=zip(food_booked,quantity_booked),flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)


@app.route('/gocart', methods=['GET', 'POST'])
@login_required
def cart():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    return render_template('gocart.html',title='Book food | FSP', form=form, cart=zip(food_booked,quantity_booked),flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)


error_vol=False
@app.route('/volunteerequest', methods=['GET', 'POST'])
def volunteerequest():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    global  error_vol
    if current_user.is_authenticated:
         form = VolunteerForm()
         points = [point.name for point in Point.query.all()]
         succes = False
         if request.method == 'POST':
             if form.validate_on_submit():
                 msg = Message(sender='contact@example.com', recipients=['foodsharingpoint@gmail.com'])
                 msg.body = """Fresh forces!!!
                %s %s is asking to becoming a volunteer in %s point          """ % (
                 current_user.first_name, current_user.last_name, request.form.get("Point"))
                 mail.send(msg)
                 flash("Thank you for your message. We'll get back to you shortly.")
                 return render_template('volunteerrequest.html',title='Become a volunteer | FSP', form=form, points=points, succes=True,flag_access_as_volunteer=flag_access_as_volunteer)

         elif request.method == 'GET':
             return render_template('volunteerrequest.html',title='Become a volunteer | FSP', form=form, succes=succes, points=points,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)

    else:
         flash("Please register before requesting to become a volunteer!")
         error_vol=True
         return redirect(url_for('signup',error_vol=error_vol))

@app.route('/volunteerpage', methods=['GET', 'POST'])
def volunteerpage():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    return render_template('volunteerpage.html',title='Become a volunteer | FSP',flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)

@app.route('/volunteerpanel', methods=['GET', 'POST'])
def volunteerpanel():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    return render_template('volunteer_panel.html',title='Volunteer Panel | FSP',flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)

@app.route('/addfood', methods=['GET', 'POST'])
def addfood():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    flag_addfood = False
    form=AddFood()
    points = [point.name for point in Point.query.all()]
    if form.validate_on_submit():
        datas=form.exp_data.data
        datetime_object = datetime.strptime(str(datas), '%Y-%m-%d')
        today = datetime.today()
        if datetime_object>=today:
            flag_addfood=True
            foodadded = FoodAvailable(type=form.type.data,point=request.form.get("Point"),availability=form.quantity.data,expired_data=datetime_object)
            db.session.add(foodadded)
            db.session.commit()
            flash("Food added successfully!")
        else:
            flag_addfood=False
            flash("Attention: You are adding a food already expired!!!")
    return render_template('add_food.html',title='Add Food | FSP',form=form,points=points,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus,flag_addfood=flag_addfood)

@app.route('/removefood', methods=['GET', 'POST'])
def removefood():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    form=RemoveFood()
    success=True
    points = [point.name for point in Point.query.all()]
    if form.validate_on_submit():
        datas=form.exp_data.data
        datetime_object = datetime.strptime(str(datas), '%Y-%m-%d')
        foodremoved = FoodAvailable.query.filter_by(type=form.type.data,point=request.form.get("Point"),expired_data=datetime_object).first()
        if foodremoved:
            success=False
            foodremoved.availability=foodremoved.availability-int(form.quantity.data)
            db.session.commit()
            flash("Food removed successfully!")
            if foodremoved.availability==0:
                FoodAvailable.query.filter_by(type=form.type.data,point=request.form.get("Point"),expired_data=datetime_object).delete()
                db.session.commit()
        else:
            success=True
            flash('Food with the indicated expired data not found in %s stock' % request.form.get("Point"))
    return render_template('remove_food.html',title='Remove Food | FSP',form=form,points=points,flag_access_as_volunteer=flag_access_as_volunteer,success=success,bonus=bonus)

@app.route('/givebonus', methods=['GET', 'POST'])
def givebonus():
    voucher = []
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    form=GiveBonus()
    success=True
    if form.validate_on_submit():
        bonuss = User.query.filter_by(first_name=form.first_name.data, last_name=form.last_name.data,
                                                    email=form.email.data).first()
        if bonuss:
            if form.bonus.data>0:
                success=False
                bonuss.bonus=bonuss.bonus+form.bonus.data
                db.session.commit()
                flash("Bonus correctly added!")
                msg = Message(sender=app.config['MAIL_USERNAME'], recipients=[form.email.data])
                msg.body = """Dear %s %s congratulations!!! You have received %d p bonus.          """ % (
                current_user.first_name, current_user.last_name, form.bonus.data)
                mail.send(msg)
                today = datetime.today()
                bonus_added = Bonus(date_bonus=today, user_id=current_user.id, bonus=form.bonus.data)
                db.session.add(bonus_added)
                db.session.commit()

            elif (form.bonus.data<0 and form.bonus.data%200==0):
                if abs(bonuss.bonus) >= abs(form.bonus.data):
                    voucher_quantity=abs(form.bonus.data)/200
                    success=False
                    bonuss.bonus=bonuss.bonus+form.bonus.data
                    db.session.commit()
                    flash("Bonus successfully converted in vouchers!")
                    msg = Message(sender=app.config['MAIL_USERNAME'], recipients=[form.email.data])
                    for i in range(voucher_quantity):
                        s=string.uppercase + string.digits
                        voucher.append(''.join(random.sample(s,10)))
                    msg.body = """Dear %s %s congratulations!!! You have received %d vouchers that you can use in our affiliated supermarkets. Here the voucher codes: %s""" % (
                    current_user.first_name, current_user.last_name, voucher_quantity, tuple(voucher))
                    mail.send(msg)
                    today = datetime.today()
                    bonus_added = Bonus(date_bonus=today, user_id=current_user.id, bonus=form.bonus.data, voucher=voucher_quantity)
                    db.session.add(bonus_added)
                    db.session.commit()
                else:
                    flash("Error: The selected user has not enough points to be converted in vouchers!")
            else:
                flash("Error: insert bonus correctly! (200 p bonus are equal to 1 voucher)")
        else:
            success=True
            flash("Sorry no user found!")
    return render_template('give_bonus.html',title='Manage bonus/voucher | FSP',form=form,flag_access_as_volunteer=flag_access_as_volunteer,success=success,bonus=bonus)

@app.route('/yourorders', methods=['GET', 'POST'])
def yourorders():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    orders=Order.query.filter_by(user_id=current_user.id).all()
    date_order=[]
    date_order_done=[]
    point_select=[]
    for order in orders:
        date_order.append(order.date_order)
        date_order_done.append(order.date_order_done)
        point_select.append(order.point)
    ordersz=zip(date_order,date_order_done,point_select)
    return render_template('your_orders.html',title='Your orders | FSP',ordersz=ordersz,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)

@app.route('/yourbonus', methods=['GET', 'POST'])
def yourbonus():
    if current_user.is_authenticated:
        bonus=current_user.bonus
    else:
        bonus=None
    bonuss=Bonus.query.filter_by(user_id=current_user.id).all()
    datebonus=[]
    voucher=[]
    bonx=[]
    for bon in bonuss:
        datebonus.append(bon.date_bonus)
        voucher.append(bon.voucher)
        bonx.append(bon.bonus)
    bonusz=zip(datebonus,bonx,voucher)
    return render_template('your_bonus.html',title='Your bonus | FSP',bonusz=bonusz,flag_access_as_volunteer=flag_access_as_volunteer,bonus=bonus)

if __name__ == '__main__':
    app.run()
