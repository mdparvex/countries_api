from rest_framework.throttling import UserRateThrottle


class TeacherUserThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            # Use a different rate for premium users
            # if request.user.profile.is_premium:
            #     self.rate = '1000/day'  # Higher limit for premium users
            # else:
            #     self.rate = '100/day'  # Default limit for regular users
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk  # Use user ID as the identifier
            }
        return None  # No throttling for unauthenticated users