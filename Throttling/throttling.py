from rest_framework.throttling import UserRateThrottle


class Custom_1(UserRateThrottle):
    scope = 'custom_1'


class Custom_2(UserRateThrottle):
    scope = 'custom_2'


class Custom_3(UserRateThrottle):
    scope = 'custom_3'