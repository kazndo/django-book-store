from django.contrib import admin
from .models import Author, Book, Order


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """著者の管理画面"""
    list_display = ('id', 'name', 'email', 'created_at', 'book_count')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('基本情報', {
            'fields': ('name', 'email')
        }),
        ('その他', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def book_count(self, obj):
        """著者の書籍数を表示"""
        return obj.books.count()
    book_count.short_description = '書籍数'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """書籍の管理画面"""
    list_display = ('id', 'title', 'author', 'isbn', 'price', 'stock', 'published_date', 'order_count')
    list_filter = ('published_date', 'author', 'created_at')
    search_fields = ('title', 'isbn', 'author__name')
    readonly_fields = ('created_at', 'updated_at', 'total_revenue')
    ordering = ('-created_at',)
    
    # リスト表示の設定
    list_per_page = 20
    list_editable = ('stock', 'price')  # リスト画面から直接編集可能
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'author', 'isbn', 'published_date')
        }),
        ('販売情報', {
            'fields': ('price', 'stock')
        }),
        ('統計情報', {
            'fields': ('total_revenue', 'order_count'),
            'classes': ('collapse',)
        }),
        ('日時情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # 著者を選択する際のフィルター
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = Author.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def order_count(self, obj):
        """注文数を表示"""
        return obj.orders.count()
    order_count.short_description = '注文数'
    
    def total_revenue(self, obj):
        """売上合計を表示"""
        from django.db.models import Sum
        total = obj.orders.aggregate(Sum('total_price'))['total_price__sum']
        return f"¥{total or 0:,.0f}"
    total_revenue.short_description = '売上合計'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """注文の管理画面"""
    list_display = ('id', 'book', 'author_name', 'quantity', 'total_price', 'order_date')
    list_filter = ('order_date', 'book__author')
    search_fields = ('book__title', 'book__author__name')
    readonly_fields = ('order_date',)
    ordering = ('-order_date',)
    
    fieldsets = (
        ('注文情報', {
            'fields': ('book', 'quantity', 'total_price')
        }),
        ('日時情報', {
            'fields': ('order_date',),
            'classes': ('collapse',)
        }),
    )
    
    def author_name(self, obj):
        """著者名を表示"""
        return obj.book.author.name
    author_name.short_description = '著者'
