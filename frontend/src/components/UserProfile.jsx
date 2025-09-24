import { useAuth0 } from '@auth0/auth0-react';

function UserProfile() {
  const { user, isAuthenticated } = useAuth0();

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="flex items-center space-x-2">
      <img
        src={user.picture}
        alt={user.name}
        className="w-8 h-8 rounded-full"
      />
      <div className="text-sm">
        <p className="font-medium text-gray-700">{user.name}</p>
        <p className="text-gray-500">{user.email}</p>
      </div>
    </div>
  );
}

export default UserProfile;