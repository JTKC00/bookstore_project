from django.core.management.base import BaseCommand
from books.models import Book
import random

class Command(BaseCommand):
    help = '重置所有書籍的庫存為隨機數量 (用於測試)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--min-stock',
            type=int,
            default=0,
            help='最小庫存數量 (預設: 0)'
        )
        parser.add_argument(
            '--max-stock',
            type=int,
            default=50,
            help='最大庫存數量 (預設: 50)'
        )
        parser.add_argument(
            '--set-stock',
            type=int,
            help='設定所有書籍為固定庫存數量'
        )

    def handle(self, *args, **options):
        min_stock = options['min_stock']
        max_stock = options['max_stock']
        set_stock = options.get('set_stock')

        books = Book.objects.all()
        updated_count = 0

        for book in books:
            if set_stock is not None:
                # 設定固定庫存
                book.stock = set_stock
            else:
                # 設定隨機庫存
                book.stock = random.randint(min_stock, max_stock)
            
            book.save()
            updated_count += 1

        if set_stock is not None:
            self.stdout.write(
                self.style.SUCCESS(
                    f'成功更新 {updated_count} 本書籍的庫存為 {set_stock}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'成功更新 {updated_count} 本書籍的庫存 (範圍: {min_stock}-{max_stock})'
                )
            )

        # 顯示一些庫存統計
        total_books = books.count()
        out_of_stock = books.filter(stock=0).count()
        low_stock = books.filter(stock__gt=0, stock__lte=5).count()
        
        self.stdout.write(f'\n庫存統計:')
        self.stdout.write(f'總書籍數: {total_books}')
        self.stdout.write(f'缺貨書籍: {out_of_stock}')
        self.stdout.write(f'低庫存書籍 (1-5本): {low_stock}')
