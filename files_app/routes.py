import os

from sanic import Blueprint
from sanic import response
from jinja2 import Template

from files_app import models
from setup import cache, Settings, db

bp = Blueprint('files_app')


async def generate_jinja_template(template: str, **kwargs) -> str:
    with open ('files_app/templates/' + template) as f:
        t = Template(f.read())
    return response.html(t.render(**kwargs))


@bp.route('/', methods=['GET', 'POST'])
async def files(request):
    files = await cache.get('files')
    if not files:
        query = models.File.select()
        files = await db.fetch_all(query=query)
        if files:
            await cache.set('files', files)

    this_response = {'success': False, 'error': False, 'files': files}

    if request.method == 'POST':
        file = request.files['file'][0]

        if file.name:
            query = models.File.insert()
            values = {'name': file.name}
            async with db.transaction():
                file_id = await db.execute(query=query, values=values)

                if not os.path.exists(Settings.get_files_dir()):
                    os.makedirs(Settings.FILES_DIR)

                with open(f'{Settings.get_files_dir()}{file_id}_{file.name}', "wb") as f:
                    f.write(file.body)

            query = models.File.select()
            files = await db.fetch_all(query=query)
            await cache.set('files', files)
            this_response.update({'success': True, 'files': files})
        else:
            this_response['error'] = 'No file name'

    return await generate_jinja_template('index.html', **this_response)


@bp.route('/files/<file_id>')
async def download_file(request, file_id):
    query = models.File.select().where(models.File.c.id == 'id_1').__str__()
    file = await db.fetch_one(query, {'id_1': file_id})
    return await response.file(f'{Settings.get_files_dir()}{file.id}_{file.name}')
