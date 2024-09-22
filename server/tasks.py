from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Todo
from extensions import db

tasks = Blueprint('tasks', __name__)

@tasks.route('/task', methods=['GET', 'POST'])
@login_required
def task_list():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, user_id=current_user.id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('tasks.task_list'))
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created).all()
        return render_template('task_list.html', tasks=tasks)

@tasks.route('/task/delete/<int:id>')
@login_required
def delete_task(id):
    task_to_delete = Todo.query.get_or_404(id)
    if task_to_delete.user_id != current_user.id:
        abort(403)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('tasks.task_list'))
    except:
        return 'There was a problem deleting that task'

@tasks.route('/task/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_task(id):
    task = Todo.query.get_or_404(id)
    if task.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect(url_for('tasks.task_list'))
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)
