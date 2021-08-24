from flask import Blueprint, render_template, flash, abort, redirect, url_for, request
from flask_login import current_user, login_required
from toDoItems.items.form import ItemForm, ItemEditForm
from toDoItems import db
from toDoItems.models import Item

items = Blueprint('items', __name__)



@items.route('/addItem/',methods=['GET', 'POST'])
@login_required
def addItem():
    form = ItemForm()
    page = request.args.get('page',1,type=int)
    allItems = Item.query.filter_by(user_id=current_user.id).order_by(Item.itemDate.desc()).paginate(page=page,per_page=5)
    if form.validate_on_submit():
        item = Item(itemName=form.itemName.data, person=current_user)
        db.session.add(item)
        db.session.commit()
        flash('One item has been added', 'info')
        return redirect(url_for('items.addItem'))
    return render_template('addItem.html', title='Add Item', form=form, allItems=allItems)



@items.route('/delete_item/item-<int:id>', methods=['GET', 'POST'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    if item.user_id != current_user.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('One list item has been deleted', 'info')
    return redirect(url_for('items.addItem'))



@items.route('/edit_item/item-<int:id>', methods=['POST','GET'])
@login_required
def edit_item(id):
    item = Item.query.get_or_404(id)
    if item.user_id != current_user.id:
        abort(403)
    form = ItemEditForm()
    if form.validate_on_submit():
        item.itemName = form.itemName.data
        db.session.commit()
        flash('One item has been updated', 'info')
        return redirect(url_for('items.addItem'))
    if request.method == "GET":
        form.itemName.data = item.itemName
    return render_template('editItem.html',title = "Edit Item", form=form)