from rest_framework import serializers 
from games.models import Game 
from games.models import GameCategory
from games.models import Player
from games.models import PlayerScore
import games.views
 
 
class GameSerializer(serializers.HyperlinkedModelSerializer):
    # We want to display the game category's name instead of the id
    game_category = serializers.SlugRelatedField(queryset=GameCategory.objects.all(), slug_field='name') 
    class Meta: 
        model = Game 
        fields = ('url',  
                  'name',  
                  'release_date', 
                  'game_category',  
                  'played') 


class GameCategorySerializer(serializers.HyperlinkedModelSerializer): 
    games = serializers.HyperlinkedRelatedField( 
        many=True, 
        read_only=True, 
        view_name='game-detail') 
 
    class Meta: 
        model = GameCategory 
        fields = ( 
            'url', 
            'pk', 
            'name', 
            'games') 

class ScoreSerilizer(serializers.HyperlinkedModelSerializer):
    # We want to display all the details for the game
    game = GameSerializer()
    # We don't include the player because it will nested in the player
    class Meta:
        model = PlayerScore
        fields = (
            'url', 
            'pk', 
            'score', 
            'score_date', 
            'game', 
        )

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerilizer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Player.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Player 
        fields = ( 
            'url', 
            'name', 
            'gender', 
            'gender_description', 
            'scores', 
            )
        
class PlayerScoreSerializer(serializers.HyperlinkedModelSerializer):
    player = serializers.SlugRelatedField(queryset=Player.objects.all(),slug_field='name')
    # We want to display the game's name insted of id
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')

    class Meta: 
        model = PlayerScore 
        fields = ( 
            'url', 
            'pk', 
            'score', 
            'score_date', 
            'player', 
            'game', 
            ) 