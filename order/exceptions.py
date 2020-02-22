class NotEnoughMoneyError(Exception):
    def __init__(self):
        super().__init__('계좌 잔액이 부족합니다.')


class OutOfStockError(Exception):
    def __init__(self):
        super().__init__('품절 상품이 존재합니다.')
