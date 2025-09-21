import React from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";

const MOCK_DEALS = [
  {
    id: "1",
    title: "$5 Wings & $4 Beer",
    venue: "The Local Pub",
    address: "123 Main St",
    category: "food",
    savings: 40,
    distance: "0.5 km",
    image: "https://via.placeholder.com/300x200",
    featured: true,
  },
  {
    id: "2",
    title: "Half Price Cocktails",
    venue: "Rooftop Lounge",
    address: "456 Queen St",
    category: "drink",
    savings: 50,
    distance: "1.2 km",
    image: "https://via.placeholder.com/300x200",
    featured: false,
  },
];

export default function HomeScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Good evening! 🌅</Text>
            <Text style={styles.location}>Toronto, ON</Text>
          </View>
          <TouchableOpacity style={styles.notificationButton}>
            <Ionicons name="notifications-outline" size={24} color="#64748B" />
          </TouchableOpacity>
        </View>

        {/* Spotlight Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>✨ Spotlight</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {MOCK_DEALS.filter((deal) => deal.featured).map((deal) => (
              <TouchableOpacity key={deal.id} style={styles.spotlightCard}>
                <Image
                  source={{ uri: deal.image }}
                  style={styles.spotlightImage}
                />
                <View style={styles.spotlightContent}>
                  <Text style={styles.spotlightTitle}>{deal.title}</Text>
                  <Text style={styles.spotlightVenue}>{deal.venue}</Text>
                  <Text style={styles.spotlightSavings}>
                    {deal.savings}% off
                  </Text>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* On Now Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🔥 On Now</Text>
          {MOCK_DEALS.map((deal) => (
            <TouchableOpacity key={deal.id} style={styles.dealCard}>
              <Image source={{ uri: deal.image }} style={styles.dealImage} />
              <View style={styles.dealContent}>
                <Text style={styles.dealTitle}>{deal.title}</Text>
                <Text style={styles.dealVenue}>{deal.venue}</Text>
                <Text style={styles.dealAddress}>{deal.address}</Text>
                <View style={styles.dealMeta}>
                  <Text style={styles.dealSavings}>{deal.savings}% off</Text>
                  <Text style={styles.dealDistance}>{deal.distance}</Text>
                </View>
              </View>
              <TouchableOpacity style={styles.favoriteButton}>
                <Ionicons name="heart-outline" size={20} color="#64748B" />
              </TouchableOpacity>
            </TouchableOpacity>
          ))}
        </View>

        {/* Starting Soon Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>⏰ Starting Soon</Text>
          <Text style={styles.emptyState}>
            Check back in a bit for upcoming deals!
          </Text>
        </View>

        {/* Categories Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>🍽️ Explore by Category</Text>
          <View style={styles.categoriesGrid}>
            {["Food", "Drinks", "Bundles", "Events"].map((category) => (
              <TouchableOpacity key={category} style={styles.categoryCard}>
                <Text style={styles.categoryText}>{category}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F8FAFC",
  },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: 20,
    backgroundColor: "#FFFFFF",
  },
  greeting: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#1E293B",
  },
  location: {
    fontSize: 14,
    color: "#64748B",
    marginTop: 4,
  },
  notificationButton: {
    padding: 8,
  },
  section: {
    marginTop: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: "bold",
    color: "#1E293B",
    paddingHorizontal: 20,
    marginBottom: 16,
  },
  spotlightCard: {
    width: 280,
    marginLeft: 20,
    backgroundColor: "#FFFFFF",
    borderRadius: 12,
    overflow: "hidden",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  spotlightImage: {
    width: "100%",
    height: 160,
  },
  spotlightContent: {
    padding: 16,
  },
  spotlightTitle: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#1E293B",
  },
  spotlightVenue: {
    fontSize: 14,
    color: "#64748B",
    marginTop: 4,
  },
  spotlightSavings: {
    fontSize: 14,
    fontWeight: "600",
    color: "#059669",
    marginTop: 8,
  },
  dealCard: {
    flexDirection: "row",
    backgroundColor: "#FFFFFF",
    marginHorizontal: 20,
    marginBottom: 12,
    borderRadius: 12,
    overflow: "hidden",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  dealImage: {
    width: 80,
    height: 80,
  },
  dealContent: {
    flex: 1,
    padding: 12,
  },
  dealTitle: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1E293B",
  },
  dealVenue: {
    fontSize: 14,
    color: "#64748B",
    marginTop: 2,
  },
  dealAddress: {
    fontSize: 12,
    color: "#94A3B8",
    marginTop: 2,
  },
  dealMeta: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 8,
  },
  dealSavings: {
    fontSize: 12,
    fontWeight: "600",
    color: "#059669",
  },
  dealDistance: {
    fontSize: 12,
    color: "#64748B",
  },
  favoriteButton: {
    padding: 12,
    justifyContent: "center",
  },
  emptyState: {
    textAlign: "center",
    color: "#64748B",
    fontStyle: "italic",
    paddingHorizontal: 20,
  },
  categoriesGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    paddingHorizontal: 20,
  },
  categoryCard: {
    width: "48%",
    backgroundColor: "#FFFFFF",
    padding: 20,
    borderRadius: 12,
    marginBottom: 12,
    marginRight: "2%",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  categoryText: {
    fontSize: 16,
    fontWeight: "600",
    color: "#1E293B",
  },
});
