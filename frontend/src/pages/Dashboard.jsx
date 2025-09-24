import { useState } from 'react';
import { useApi } from '../hooks/useApi';
import { dashboardService } from '../services';

function Dashboard() {
  const [timeRange, setTimeRange] = useState('30d');
  const [refreshKey, setRefreshKey] = useState(0);

  // Fetch dashboard overview with all statistics
  const { data: dashboardData, loading: dashboardLoading, error: dashboardError } = useApi(
    () => dashboardService.getOverview(),
    [refreshKey]
  );

  // Fetch analytics with time range dependency
  const { data: opportunitiesAnalytics, loading: oppsLoading } = useApi(
    () => dashboardService.getOpportunitiesAnalytics(timeRange),
    [timeRange, refreshKey]
  );

  const { data: proposalsAnalytics, loading: propsLoading } = useApi(
    () => dashboardService.getProposalsAnalytics(timeRange),
    [timeRange, refreshKey]
  );

  const { data: campaignsAnalytics, loading: campsLoading } = useApi(
    () => dashboardService.getCampaignsAnalytics(timeRange),
    [timeRange, refreshKey]
  );

  const loading = dashboardLoading || oppsLoading || propsLoading || campsLoading;
  const error = dashboardError;

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  const StatCard = ({ title, value, icon, color, loading }) => (
    <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <div className={`w-8 h-8 ${color} rounded-md flex items-center justify-center`}>
            <span className="text-white text-sm">{icon}</span>
          </div>
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">
            {loading ? (
              <div className="animate-pulse bg-gray-200 h-6 w-12 rounded"></div>
            ) : (
              value || 0
            )}
          </p>
        </div>
      </div>
    </div>
  );

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="mb-4">
          <svg className="mx-auto h-12 w-12 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">Unable to load dashboard</h3>
        <p className="text-gray-500 mb-4">Make sure the backend server is running on localhost:8000</p>
        <button
          onClick={handleRefresh}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div>
      {/* Header with controls */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome to your MapMyClient dashboard</p>
        </div>
        <div className="mt-4 sm:mt-0 flex items-center space-x-4">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
          </select>
          <button
            onClick={handleRefresh}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-md text-sm flex items-center"
            disabled={loading}
          >
            <svg className={`w-4 h-4 mr-1 ${loading ? 'animate-spin' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Opportunities"
          value={dashboardData?.statistics?.opportunities_count}
          icon="📝"
          color="bg-blue-500"
          loading={loading}
        />
        <StatCard
          title="Total Proposals"
          value={dashboardData?.statistics?.proposals_count}
          icon="📄"
          color="bg-green-500"
          loading={loading}
        />
        <StatCard
          title="Active Campaigns"
          value={dashboardData?.statistics?.campaigns_count}
          icon="📢"
          color="bg-purple-500"
          loading={loading}
        />
        <StatCard
          title="LinkedIn Posts"
          value={dashboardData?.statistics?.posts_count}
          icon="💼"
          color="bg-indigo-500"
          loading={loading}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Opportunities */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Recent Opportunities</h2>
          </div>
          <div className="p-6">
            {loading ? (
              <div className="space-y-3">
                {[...Array(5)].map((_, i) => (
                  <div key={i} className="animate-pulse flex items-center space-x-4">
                    <div className="w-2 h-2 bg-gray-200 rounded-full"></div>
                    <div className="flex-1 h-4 bg-gray-200 rounded"></div>
                    <div className="w-16 h-4 bg-gray-200 rounded"></div>
                  </div>
                ))}
              </div>
            ) : dashboardData?.recent_opportunities?.length > 0 ? (
              <ul className="space-y-3">
                {dashboardData.recent_opportunities.map((opportunity) => (
                  <li key={opportunity.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
                    <div className="flex items-center space-x-3">
                      <div className={`w-2 h-2 rounded-full ${
                        opportunity.status === 'won' ? 'bg-green-500' :
                        opportunity.status === 'lost' ? 'bg-red-500' :
                        opportunity.status === 'sent' ? 'bg-blue-500' : 'bg-gray-400'
                      }`}></div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">{opportunity.title}</p>
                        <p className="text-xs text-gray-500">{opportunity.company_name || 'No company'}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">{opportunity.budget_range || 'No budget'}</p>
                      <p className="text-xs text-gray-500 capitalize">{opportunity.status}</p>
                    </div>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-center py-8">No opportunities yet</p>
            )}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
          </div>
          <div className="p-6 space-y-3">
            <button className="w-full text-left p-3 rounded-md hover:bg-gray-50 transition-colors">
              <div className="font-medium text-gray-900">📊 Create Opportunity</div>
              <div className="text-sm text-gray-500">Add a new business opportunity</div>
            </button>
            <button className="w-full text-left p-3 rounded-md hover:bg-gray-50 transition-colors">
              <div className="font-medium text-gray-900">📄 Generate Proposal</div>
              <div className="text-sm text-gray-500">AI-powered proposal creation</div>
            </button>
            <button className="w-full text-left p-3 rounded-md hover:bg-gray-50 transition-colors">
              <div className="font-medium text-gray-900">📢 New Campaign</div>
              <div className="text-sm text-gray-500">Start an outreach campaign</div>
            </button>
            <button className="w-full text-left p-3 rounded-md hover:bg-gray-50 transition-colors">
              <div className="font-medium text-gray-900">📝 Import LinkedIn Posts</div>
              <div className="text-sm text-gray-500">Analyze new opportunities</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;