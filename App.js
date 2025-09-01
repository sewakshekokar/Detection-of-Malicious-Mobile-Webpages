// D. Code for User Interface using React Native
import React, { Component } from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

function HomeScreen({ navigation }) {
  const [text, setText] = React.useState("Enter URL");

  const onButtonPress = async () => {
  console.log("Sending request to:", text);
  try {
    const response = await fetch('https://7ca2-202-3-77-210.ngrok-free.app/abc', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: text })
    });
    const result = await response.json();
    console.log("Response:", result);
    navigation.navigate('Result', { response: result });
  } catch (error) {
    console.log("Error:", error);
    alert("Something went wrong. Check server and URL.");
  }
};


  return (
    <View style={styles.container}>
      <TextInput style={styles.input} onChangeText={setText} value={text} />
      <Button title="Check URL" onPress={onButtonPress} />
    </View>
  );
}

function ResultScreen({ route, navigation }) {
  const { response } = route.params;
  return (
    <View style={styles.container}>
      <Text>{response}</Text>
      <Button title="Go back" onPress={() => navigation.goBack()} />
    </View>
  );
}

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Result" component={ResultScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    margin: 10
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10
  }
});
