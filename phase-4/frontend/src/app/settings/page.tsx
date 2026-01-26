'use client';

/**
 * Settings page with profile and password management.
 * Protected route - requires authentication.
 */

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/auth/AuthProvider';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Sidebar } from '@/components/ui/Sidebar';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { ErrorMessage } from '@/components/ui/ErrorMessage';
import { updateProfile, changePassword, ApiError } from '@/lib/api';
import { VALIDATION } from '@/lib/constants';

// Icons
const UserIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>
);

const LockIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
  </svg>
);

const CheckIcon = () => (
  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
  </svg>
);

export default function SettingsPage() {
  const router = useRouter();
  const { auth, updateUser } = useAuth();

  // Profile form state
  const [name, setName] = useState('');
  const [profileError, setProfileError] = useState<string | null>(null);
  const [profileSuccess, setProfileSuccess] = useState(false);
  const [isUpdatingProfile, setIsUpdatingProfile] = useState(false);

  // Password form state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [passwordSuccess, setPasswordSuccess] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  // Initialize name from auth
  useEffect(() => {
    if (auth.user?.name) {
      setName(auth.user.name);
    }
  }, [auth.user?.name]);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!auth.isLoading && !auth.isAuthenticated) {
      router.replace('/login');
    }
  }, [auth.isLoading, auth.isAuthenticated, router]);

  // Handle profile update
  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileError(null);
    setProfileSuccess(false);

    if (name && name.length > VALIDATION.name.maxLength) {
      setProfileError(VALIDATION.name.message);
      return;
    }

    setIsUpdatingProfile(true);

    try {
      const response = await updateProfile({ name: name || undefined });
      updateUser({ name: response.name || undefined });
      setProfileSuccess(true);
      setTimeout(() => setProfileSuccess(false), 3000);
    } catch (err) {
      if (err instanceof ApiError) {
        setProfileError(err.detail);
      } else {
        setProfileError('Failed to update profile. Please try again.');
      }
    } finally {
      setIsUpdatingProfile(false);
    }
  };

  // Handle password change
  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);
    setPasswordSuccess(false);

    // Validate
    if (!currentPassword) {
      setPasswordError('Current password is required');
      return;
    }

    if (!newPassword) {
      setPasswordError('New password is required');
      return;
    }

    if (newPassword.length < VALIDATION.password.minLength) {
      setPasswordError(VALIDATION.password.message);
      return;
    }

    if (newPassword !== confirmPassword) {
      setPasswordError('New passwords do not match');
      return;
    }

    setIsChangingPassword(true);

    try {
      await changePassword({
        current_password: currentPassword,
        new_password: newPassword,
      });
      setPasswordSuccess(true);
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => setPasswordSuccess(false), 3000);
    } catch (err) {
      if (err instanceof ApiError) {
        setPasswordError(err.detail);
      } else {
        setPasswordError('Failed to change password. Please try again.');
      }
    } finally {
      setIsChangingPassword(false);
    }
  };

  // Show loading while checking auth
  if (auth.isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Don't render if not authenticated (will redirect)
  if (!auth.isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen flex bg-gray-50">
      {/* Sidebar */}
      <Sidebar activeItem="settings" />

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm px-4 lg:px-6 py-4 flex-shrink-0">
          <div className="flex items-center">
            <h1 className="text-xl lg:text-2xl font-bold ml-12 lg:ml-0">
              <span className="text-red-500">To</span>
              <span className="text-gray-800">-Do</span>
            </h1>
          </div>
        </header>

        {/* Main content area */}
        <main className="flex-1 p-4 lg:p-6 overflow-auto bg-gray-50">
          {/* Page Title */}
          <div className="mb-6">
            <h2 className="text-xl lg:text-2xl font-bold text-gray-800">Settings</h2>
            <p className="text-gray-500 mt-1 text-sm lg:text-base">Manage your profile and account settings</p>
          </div>

          <div className="max-w-2xl space-y-6">
            {/* Profile Section */}
            <div className="bg-white rounded-xl shadow-card p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-blue-100 flex items-center justify-center">
                  <UserIcon />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-800">Profile Information</h3>
                  <p className="text-sm text-gray-500">Update your display name</p>
                </div>
              </div>

              {profileError && (
                <div className="mb-4">
                  <ErrorMessage message={profileError} onDismiss={() => setProfileError(null)} />
                </div>
              )}

              {profileSuccess && (
                <div className="mb-4 flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700">
                  <CheckIcon />
                  <span>Profile updated successfully!</span>
                </div>
              )}

              <form onSubmit={handleProfileUpdate} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={auth.user?.email || ''}
                    disabled
                    className="w-full px-4 py-3 bg-gray-100 border border-gray-200 rounded-lg text-gray-500 cursor-not-allowed"
                  />
                  <p className="mt-1 text-xs text-gray-400">Email cannot be changed</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Display Name</label>
                  <Input
                    type="text"
                    name="name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter your display name"
                    icon={<UserIcon />}
                    maxLength={255}
                  />
                </div>

                <div className="flex justify-end">
                  <Button
                    type="submit"
                    variant="primary"
                    isLoading={isUpdatingProfile}
                    disabled={isUpdatingProfile}
                  >
                    Save Changes
                  </Button>
                </div>
              </form>
            </div>

            {/* Password Section */}
            <div className="bg-white rounded-xl shadow-card p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-lg bg-red-100 flex items-center justify-center">
                  <LockIcon />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-800">Change Password</h3>
                  <p className="text-sm text-gray-500">Update your account password</p>
                </div>
              </div>

              {passwordError && (
                <div className="mb-4">
                  <ErrorMessage message={passwordError} onDismiss={() => setPasswordError(null)} />
                </div>
              )}

              {passwordSuccess && (
                <div className="mb-4 flex items-center gap-2 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700">
                  <CheckIcon />
                  <span>Password changed successfully!</span>
                </div>
              )}

              <form onSubmit={handlePasswordChange} className="space-y-4">
                <Input
                  type="password"
                  name="currentPassword"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  placeholder="Current Password"
                  icon={<LockIcon />}
                  autoComplete="current-password"
                />

                <Input
                  type="password"
                  name="newPassword"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="New Password (min 8 characters)"
                  icon={<LockIcon />}
                  autoComplete="new-password"
                />

                <Input
                  type="password"
                  name="confirmPassword"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm New Password"
                  icon={<LockIcon />}
                  autoComplete="new-password"
                />

                <div className="flex justify-end">
                  <Button
                    type="submit"
                    variant="primary"
                    isLoading={isChangingPassword}
                    disabled={isChangingPassword}
                  >
                    Change Password
                  </Button>
                </div>
              </form>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
