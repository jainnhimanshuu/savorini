import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";

export default function RootLayout() {
  return (
    <>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="venue/[id]" options={{ title: "Venue Details" }} />
        <Stack.Screen name="deal/[id]" options={{ title: "Deal Details" }} />
      </Stack>
      <StatusBar style="auto" />
    </>
  );
}
