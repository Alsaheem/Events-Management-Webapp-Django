from django import forms
from event.models import Comment,Event


class EventForm(forms.ModelForm):

    class Meta():
        model = Event
        fields = ('title','description','event_time','location','category','google_map_link','event_image1','event_image2','event_image3','due_date')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textrea postcontent'})
        }


                                              
class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        # fields = ('author','text')
        fields = ('comment_text',)

        widget = {
            # 'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textrea'})
        }
