import colorgram
from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some_random_key'
bootstrap = Bootstrap(app)


class PhotoForm(FlaskForm):
    file_to_upload = FileField('Select Image', validators=[DataRequired()])
    submit = SubmitField('Extract Colors')


def rgb_to_hex(rgb):
    return f"#{'%02x%02x%02x' % rgb}"


@app.route("/", methods=["GET", "POST"])
def home():
    form = PhotoForm()
    if form.validate_on_submit():
        image = form.file_to_upload.data
        colors = colorgram.extract(image, 10)
        color_list = []
        for color in colors:
            r = color.rgb.r
            g = color.rgb.g
            b = color.rgb.b
            new_color = (r, g, b)
            color_list.append(new_color)
        hex_list = [rgb_to_hex(color) for color in color_list]
        return render_template("index.html", form=form, colors=hex_list)
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

