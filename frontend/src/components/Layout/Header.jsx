import { useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import UserProfile from '../UserProfile';
import LogoutButton from '../LogoutButton';

function Header({ onMenuToggle }) {
  const { user, isAuthenticated } = useAuth0();
  const [isUserMenuOpen, setIsUserMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="flex items-center justify-between px-4 py-3">
        {/* Left side: Menu button and logo (mobile) */}
        <div className="flex items-center">
          <button
            onClick={onMenuToggle}
            className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <span className="sr-only">Open sidebar</span>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Logo for mobile */}
          <div className="lg:hidden ml-2">
            <span className="text-xl font-bold text-gray-900">MapMyClient</span>
          </div>
        </div>

        {/* Right side: User menu */}
        <div className="flex items-center space-x-4">
          {/* Notifications (placeholder) */}
          <button className="p-2 text-gray-400 hover:text-gray-600 relative">
            <span className="sr-only">Notifications</span>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-5 5v-5zM12 18.07a10 10 0 01-7.071-2.929 1 1 0 00-1.414 1.414A12 12 0 0012 21a12 12 0 008.485-3.515 1 1 0 00-1.414-1.414A10 10 0 0112 18.07z" />
            </svg>
            {/* Notification badge (placeholder) */}
            <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
              3
            </span>
          </button>

          {/* User menu */}
          {isAuthenticated && (
            <div className="relative">
              <button
                onClick={() => setIsUserMenuOpen(!isUserMenuOpen)}
                className="flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <img
                  src={user?.picture}
                  alt={user?.name}
                  className="w-8 h-8 rounded-full"
                />
                <svg className="ml-2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {/* User dropdown menu */}
              {isUserMenuOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                  <div className="px-4 py-3 border-b">
                    <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                    <p className="text-sm text-gray-500">{user?.email}</p>
                  </div>
                  <div className="py-1">
                    <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 w-full text-left">
                      Profile Settings
                    </button>
                    <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 w-full text-left">
                      Billing
                    </button>
                    <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 w-full text-left">
                      Help & Support
                    </button>
                    <div className="border-t border-gray-100">
                      <div className="px-4 py-2">
                        <LogoutButton />
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Close user menu when clicking outside */}
      {isUserMenuOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsUserMenuOpen(false)}
        />
      )}
    </header>
  );
}

export default Header;