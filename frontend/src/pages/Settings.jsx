function Settings() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600">Manage your account and application settings</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Settings */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Profile Settings</h2>
            </div>
            <div className="p-6">
              <p className="text-gray-500">Profile configuration will be implemented here.</p>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div>
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                <button className="w-full text-left p-3 rounded-md hover:bg-gray-50">
                  <div className="font-medium">API Settings</div>
                  <div className="text-sm text-gray-500">Configure integrations</div>
                </button>
                <button className="w-full text-left p-3 rounded-md hover:bg-gray-50">
                  <div className="font-medium">Notifications</div>
                  <div className="text-sm text-gray-500">Email preferences</div>
                </button>
                <button className="w-full text-left p-3 rounded-md hover:bg-gray-50">
                  <div className="font-medium">Export Data</div>
                  <div className="text-sm text-gray-500">Download your data</div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;