from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
import datetime as dt

from users.models import User
from reviews.models import Title, Category, Genre, Comment, Review


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=512)


class UserSignUpSerializer(serializers.Serializer):

    username = serializers.CharField(
        validators=(UnicodeUsernameValidator(),),
        max_length=150
    )

    email = serializers.EmailField(max_length=254)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if username.lower() == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя.')
        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Введенное вами имя пользователя уже занято.'
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Введенный вами адрес электронной почты уже занят.'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор категорий произведений. """
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор жанров произведений. """
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """ Сериализатор произведений, методы GET и DEL. """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class TitleCreateUpdateSerializer(serializers.ModelSerializer):
    """ Сериализатор произведений, методы POST и PATCH. """
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name'
    )

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(title_id=title_id, author=author).exists():
            raise serializers.ValidationError(
                'У Вас уже есть отзыв на это произведение.'
            )
        return data

    def validate_score(self, data):
        if data < 1 or data > 10:
            raise serializers.ValidationError(
                'Поставьте оценку в диапазоне от одного до десяти.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'review', 'pub_date')
