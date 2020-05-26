# Generated by Django 3.0.4 on 2020-03-28 17:24

from django.db import migrations
import re

MATCH_NONWORD_CHARACTERS_BEGINNING = re.compile('^\\W+')
MATCH_NONWORD_CHARACTERS_END = re.compile('\\W+$')


def clean_word(word):
    return MATCH_NONWORD_CHARACTERS_BEGINNING.sub(
        "", MATCH_NONWORD_CHARACTERS_END.sub("", word))


def ensure_word(item, word, reverse, DictionaryItem, meaning=""):
    word = clean_word(word)
    course = item.skill.module.course
    try:
        DictionaryItem.objects.get(
            course=course,
            word__iexact=word,
            reverse=reverse)
    except BaseException:
        DictionaryItem.objects.create(
            course=course,
            word=word,
            reverse=reverse,
            definition=meaning)


def forwards_func(apps, schema_editor):
    LearnSentence = apps.get_model("course", "LearnSentence")
    LearnWord = apps.get_model("course", "LearnWord")
    DictionaryItem = apps.get_model("course", "DictionaryItem")
    db_alias = schema_editor.connection.alias

    for item in LearnWord.objects.using(db_alias).all():
        for word in item.formInTargetLanguage.split():
            ensure_word(
                item,
                word,
                False,
                DictionaryItem,
                item.meaningInSourceLanguage)

        for word in item.meaningInSourceLanguage.split():
            ensure_word(
                item,
                word,
                True,
                DictionaryItem,
                item.formInTargetLanguage)

    for item in LearnSentence.objects.using(db_alias).all():
        for word in item.formInTargetLanguage.split():
            ensure_word(item, word, False, DictionaryItem)

        for word in item.meaningInSourceLanguage.split():
            ensure_word(item, word, True, DictionaryItem)


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0027_auto_20200326_2204'),
    ]

    operations = [
        migrations.RunPython(forwards_func)
    ]