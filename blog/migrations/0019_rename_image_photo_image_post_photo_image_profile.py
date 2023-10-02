# Generated by Django 4.2.4 on 2023-09-28 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_photo_options_remove_photo_post_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='image',
            new_name='image_post',
        ),
        migrations.AddField(
            model_name='photo',
            name='image_profile',
            field=models.ImageField(default='uploads/blog/post/IMG_3349.jpg', upload_to='uploads/blog/profile'),
        ),
    ]
